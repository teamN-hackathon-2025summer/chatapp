document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle_sidebar");

    toggleBtn.addEventListener("click", () => {
        // PCでは hiddenクラス、小画面では showクラスで切替
        if (window.innerWidth > 768) {
            sidebar.classList.toggle("hidden");
        } else {
            sidebar.classList.toggle("show");
        }
    });

    // 折り畳みフォーム切替
    document.querySelectorAll(".toggle_form_btn").forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");
            const targetForm = document.getElementById(targetId);
            if (targetForm) {
                targetForm.style.display =
                    targetForm.style.display === "block" ? "none" : "block";
            }
        });
    });
});
