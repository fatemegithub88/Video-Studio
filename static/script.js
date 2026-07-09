const API_BASE = "";
/* =========================
Helpers
========================= */

function $(id) {
    return document.getElementById(id);
}

function setButtonLoading(btn, isLoading, text = "Processing...") {

    if (!btn) return;

    if (isLoading) {

        btn.dataset.originalText = btn.innerText;
        btn.innerText = text;
        btn.disabled = true;
        btn.style.opacity = "0.7";

    } else {

        btn.innerText = btn.dataset.originalText || btn.innerText;
        btn.disabled = false;
        btn.style.opacity = "1";

    }

}

/* =========================
POST
========================= */

async function postData(url, data) {

    const res = await fetch(API_BASE + url, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    if (!res.ok) {

        const text = await res.text();

        throw new Error(text || "Request failed");

    }

    return await res.json();

}

/* =========================
PLYR
========================= */

let player = null;

function showPreview(url, type = "video") {

    const video = $("preview-video");
    const audio = $("preview-audio");
    const download = $("download-link");


    const previewUrl = url + "?t=" + Date.now();


    if (player) {
        player.destroy();
        player = null;
    }

    video.style.display = "none";
    audio.style.display = "none";

    if (type === "audio") {

        audio.pause();
        audio.src = previewUrl;
        audio.load();

        audio.style.display = "block";

        player = new Plyr(audio);

    } else {

        video.pause();
        video.src = previewUrl;
        video.load();

        video.style.display = "block";

        player = new Plyr(video);

    }

    download.href = previewUrl;
    download.style.display = "inline-block";
}

/* =========================
Subtitle
========================= */

async function subtitleVideo() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Generating...");

        const data = await postData("/subtitle", {

            url: $("sub-url").value

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Extract Audio
========================= */

async function extractAudio() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Extracting...");

        const data = await postData("/extract-audio", {

            url: $("audio-url").value,
            format: $("audio-format").value

        });

        showPreview(data.preview, "audio");

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Quality
========================= */

async function changeQuality() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Converting...");

        const data = await postData("/change-quality", {

            url: $("quality-url").value,
            quality: $("quality-level").value

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Compress
========================= */

async function compressVideo() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Compressing...");

        const data = await postData("/compress-video", {

            url: $("compress-url").value,
            level: $("compress-level").value

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Audio Boost
========================= */

async function audioBoost() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Boosting...");

        const data = await postData("/audio-boost", {

            url: $("boost-url").value,
            volume: parseFloat($("boost-volume").value)

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Noise Remove
========================= */

async function noiseRemove() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Cleaning...");

        const data = await postData("/noise-remove", {

            url: $("noise-url").value

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Trim
========================= */

async function trimVideo() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Trimming...");

        const data = await postData("/trim-video", {

            url: $("trim-url").value,
            start: Number($("trim-start").value),
            end: Number($("trim-end").value)

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

/* =========================
Convert
========================= */

async function convertVideo() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Converting...");

        const data = await postData("/convert-video", {

            url: $("convert-url").value,
            format: $("convert-format").value

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}

async function changeSpeed() {

    const btn = event.target;

    try {

        setButtonLoading(btn, true, "Changing...");

        const data = await postData("/change-speed", {

            url: $("speed-url").value,
            speed: parseFloat($("speed-value").value)

        });

        showPreview(data.preview);

    }

    // catch (err) {

    //     alert(err.message);

    // }

    finally {

        setButtonLoading(btn, false);

    }

}
