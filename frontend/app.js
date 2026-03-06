// 1. Configuration & Éléments du DOM
const API_URL = 'http://localhost:8000';

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const resetBtn = document.getElementById('resetBtn');
const downloadBtn = document.getElementById('downloadBtn');
const status = document.getElementById('status');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const playbackContainer = document.getElementById('playbackContainer');
const audioPlayback = document.getElementById('audioPlayback');
const processingSection = document.querySelector('.processing-section');
const resultsContainer = document.getElementById('resultsContainer');

let mediaRecorder;
let audioChunks = [];
let audioBlob;

// 2. Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) throw new Error();
        console.log('✅ Backend connecté');
    } catch (e) {
        showError('❌ Le serveur backend ne répond pas. Lance-le avec uvicorn !');
    }

    recordBtn.addEventListener('click', startRecording);
    stopBtn.addEventListener('click', stopRecording);
    resetBtn.addEventListener('click', resetRecording);
    downloadBtn.addEventListener('click', downloadImage);
});

// 3. Logique d'enregistrement
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

        mediaRecorder.onstop = async () => {
            audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            audioPlayback.src = URL.createObjectURL(audioBlob);
            playbackContainer.classList.remove('hidden');
            
            // On lance le traitement automatiquement
            await processAudio();
        };

        mediaRecorder.start();
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        status.textContent = '🔴 Enregistrement en cours...';
        status.className = 'status recording';
    } catch (e) {
        showError("Microphone non accessible. Vérifiez les autorisations.");
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        recordBtn.disabled = false;
        stopBtn.disabled = true;
        status.textContent = '✅ Enregistré !';
        status.className = 'status success';
    }
}

// 4. LE COEUR DU SYSTÈME (La fonction qui posait problème)
async function processAudio() {
    try {
        // Affiche la zone de travail
        processingSection.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        document.querySelector('.progress-steps').classList.remove('hidden');
        document.querySelector('.processing-card h2').textContent = "⚙️ Traitement en cours...";
        hideError();

        // Conversion audio
        const base64Audio = await blobToBase64(audioBlob);

        // Étapes visuelles
        updateStepStatus('step-transcript', '⏳');
        updateStepStatus('step-moderation', '⏳');
        updateStepStatus('step-enrichment', '⏳');
        updateStepStatus('step-generation', '⏳');

        // Envoi au serveur
        const response = await fetch(`${API_URL}/process`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ audio_base64: base64Audio })
        });

        if (!response.ok) throw new Error(`Erreur serveur: ${response.status}`);
        const result = await response.json();

        // Maj des coches vertes
        updateStepStatus('step-transcript', '✅');
        updateStepStatus('step-moderation', '✅');
        updateStepStatus('step-enrichment', '✅');
        updateStepStatus('step-generation', '✅');

        // --- TRANSITION VISUELLE ---
        // On cache les sabliers et on montre le résultat
        document.querySelector('.progress-steps').classList.add('hidden');
        document.querySelector('.processing-card h2').textContent = "✨ Vision de Marseille 2050";
        
        displayResults(result);

    } catch (e) {
        console.error(e);
        showError(`Erreur lors du traitement : ${e.message}`);
        processingSection.classList.add('hidden');
    }
}

// 5. Fonctions utilitaires
function updateStepStatus(stepId, status) {
    const el = document.getElementById(stepId);
    if (el) el.textContent = status;
}

function displayResults(result) {
    document.getElementById('originalText').textContent = result.original_text;
    document.getElementById('enrichedPrompt').textContent = result.enriched_prompt;
    const img = document.getElementById('generatedImage');
    img.src = result.image_url;
    
    resultsContainer.classList.remove('hidden');
}

function blobToBase64(blob) {
    return new Promise((resolve, _) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.readAsDataURL(blob);
    });
}

function resetRecording() {
    location.reload(); // Solution la plus propre pour tout remettre à zéro
}

function downloadImage() {
    const link = document.createElement('a');
    link.href = document.getElementById('generatedImage').src;
    link.download = `marseille-2050-${Date.now()}.png`;
    link.click();
}

function showError(m) { errorMessage.textContent = m; errorContainer.classList.remove('hidden'); }
function hideError() { errorContainer.classList.add('hidden'); }