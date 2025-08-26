document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle_sidebar");

    // 開閉補助
    const openDesktop = () => {
        sidebar.classList.remove("hidden");
        document.body.classList.add("sidebar_open");
    };
    const closeDesktop = () => {
        sidebar.classList.add("hidden");
        document.body.classList.remove("sidebar_open");
    };
    const openMobile = () => {
        sidebar.classList.add("show");
        document.body.classList.add("sidebar_open");
    };
    const closeMobile = () => {
        sidebar.classList.remove("show");
        document.body.classList.remove("sidebar_open");
    };

    // トグルボタン
    // PCでは hiddenクラス、小画面では showクラスで切替
    toggleBtn.addEventListener("click", () => {
        if (window.innerWidth > 768) {
            // PC：hiddenクラスで切替＋bodyにフラグ
            if (sidebar.classList.contains("hidden")) {
                openDesktop();
            } else {
                closeDesktop();
            }
        } else {
            // モバイル：showクラスで切替＋bodyにフラグ
            if (sidebar.classList.contains("show")) {
                closeMobile();
            } else {
                openMobile();
            }
        }
    });

    // 画面幅が変わったときの整合性（例：回転）
    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            // PCに戻ったらモバイル状態を解除
            sidebar.classList.remove("show");
            document.body.classList.remove("sidebar_open");
            // デスクトップは既定表示にしたいなら以下で制御
            // openDesktop();
        } else {
            // モバイルに戻ったらデスクトップ状態を解除
            sidebar.classList.remove("hidden");
            document.body.classList.remove("sidebar_open");
            // 既定は隠す
            // closeMobile();
        }
    });
});

// チャンネル作成フォーム：開く
document.querySelectorAll(".toggle_form_btn, .btn_link, .danger").forEach(button => {
    button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        if (!targetId) return;
        const targetForm = document.getElementById(targetId);
        if (targetForm) {
            const showing = targetForm.style.display === "block";
            targetForm.style.display = showing ? "none" : "block";
            targetForm.setAttribute("aria-hidden", showing ? "true" : "false");
        }
    });
});

// フォーム：閉じるボタン
document.querySelectorAll(".close_btn").forEach(button => {
    button.addEventListener("click", () => {
        const targetId = button.getAttribute("data-target");
        if (!targetId) return;
        const targetForm = document.getElementById(targetId);
        if (targetForm) {
            targetForm.style.display = "none";
            targetForm.setAttribute("aria-hidden", "true");
        }
    });
});