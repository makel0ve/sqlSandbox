async function upload_database(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/uploadDB", {
        method: "POST",
        body: formData,
    });
    if (response.ok) {
        const filename = encodeURIComponent(file.name);
        const lastDot = filename.lastIndexOf(".");
        const nameWithoutLastDot = filename.substring(0, lastDot);
        window.location.href = `/${nameWithoutLastDot}`;
    } else {
        console.log("Error: ", response.statusText);
    }
}

async function openFilePicker() {
    try {
        const pickerOpts = {
            types: [
                {
                    accept: {
                        "application/x-sqlite3": [".sqlite", ".db"],
                        "application/vnd.sqlite3": [".sqlite", ".db"],
                    },
                },
            ],
            excludeAcceptAllOption: true,
            multiple: false,
            startIn: "desktop",
        };
        const [fileHandle] = await window.showOpenFilePicker(pickerOpts);
        const file = await fileHandle.getFile();
        await upload_database(file);
    } catch (e) {
        if (e.name === "AbortError") {
            console.log("Зафиксирована отмена! Отменяем действия!");
        }
    }
}
