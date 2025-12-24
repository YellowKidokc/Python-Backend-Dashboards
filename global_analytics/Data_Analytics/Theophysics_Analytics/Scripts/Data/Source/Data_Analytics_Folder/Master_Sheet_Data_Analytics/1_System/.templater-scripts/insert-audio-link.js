// Insert Audio Link Template
async function insertAudioLink(tp) {
    // Prompt for the audio link URL
    const audioUrl = await tp.system.prompt("Enter the audio file URL (Google Drive, etc.):");
    
    if (!audioUrl) {
        new Notice('No URL provided - audio link not inserted');
        return '';
    }
    
    // Return the formatted audio callout
    return `---

> 🎧 **Prefer to listen?** [Click here to have this paper read to you](${audioUrl})

---`;
}

module.exports = insertAudioLink;
