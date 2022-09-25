var dirty = false;

function setDirty(delta, oldDelta, source) {
    dirty = true;
}

function saveCallback() {
    if (dirty) {
        var contents = quill.getContents();
        fetch("/update", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(contents)
        })
        .then((response) => response.json())
        .then((data) => {
            //noop
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        dirty = false;
    }
}

