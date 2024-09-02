async function load_page() {
    require.config({ paths: { vs: "/static/monaco-editor/min/vs" } });
    require(["vs/editor/editor.main"], function () {
        var editor = monaco.editor.create(
            document.getElementById("editor-container"),
            {
                language: "sql",
                theme: "vs",
                minimap: { enabled: false },
                automaticLayout: true,
            }
        );
        var overlayWidget = {
            domNode: (function () {
                var domNode = document.createElement("i");
                domNode.style.display = "inline-block";
                domNode.style.border = "solid black";
                domNode.style.borderWidth = "0 5px 5px 0";
                domNode.style.padding = "5px";
                domNode.style.transform = "rotate(-45deg)";
                domNode.id = "myButton";
                domNode.title = "Выполнить";
                domNode.style.right = "30px";
                domNode.style.top = "30px";
                domNode.addEventListener("mouseover", function () {
                    this.style.opacity = "0.5";
                });
                domNode.addEventListener("mouseout", function () {
                    this.style.opacity = "1";
                });
                return domNode;
            })(),
            getId: function () {
                return "my.overlay.widget";
            },
            getDomNode: function () {
                return this.domNode;
            },
            getPosition: function () {
                return null;
            },
        };
        editor.addOverlayWidget(overlayWidget);
        monaco.languages.registerCompletionItemProvider("sql", {
            provideCompletionItems: function (model, position) {},
        });
        document
            .getElementById("myButton")
            .addEventListener("click", () => sqlquery(editor.getValue()));
    });
    await create_but();
}

async function create_but() {
    let btns = document.querySelectorAll(".choices-table");
    btns.forEach((btn) => {
        btn.addEventListener("click", () => choice_table(btn.value));
    });
    let max_width = 0;
    for (let i = 0; i < btns.length; i++) {
        let width = btns[i].offsetWidth;
        if (max_width < width) {
            max_width = width;
        }
    }
    btns[btns.length - 1].style.border = "2px solid #2c2c2c";
    btns[btns.length - 1].style.backgroundColor = "rgba(189, 190, 189, 0.5)";
    btns.forEach(function (value) {
        value.style.width = `${max_width + max_width / btns.length}px`;
    });
}

async function style_but(btn) {
    let btns = document.querySelectorAll(".choices-table");
    btns.forEach(function (value) {
        if (value.value == btn) {
            value.style.border = "2px solid #2c2c2c";
            value.style.backgroundColor = "rgba(189, 190, 189, 0.5)";
        } else {
            value.style.border = "1px solid #dddddd";
            value.style.backgroundColor = "rgba(189, 190, 189, 1)";
        }
    });
}

async function choice_table(btn) {
    await style_but(btn);
    const response = await fetch("/choice_table", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: btn,
        }),
    });
    if (response.ok) {
        const html = await response.text();
        document.getElementById("table-div").innerHTML = html;
    } else {
        console.log("Error: ", response.statusText);
    }
}

async function sqlquery(value) {
    const response = await fetch("/sqlquery", {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: value,
        }),
    });
    if (response.ok) {
        const html = await response.text();
        document.getElementById("table-div").innerHTML = html;
        table_name = document.getElementById("table_name").innerHTML;
        await style_but(table_name);
    } else {
        console.log("Error: ", response.statusText);
    }
}
