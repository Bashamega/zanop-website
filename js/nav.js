
class SiteNavbar extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
            <header class="main glass">
                <a href="/" id="logo">
                    <img id="h-img" src="assets/logo.svg" alt="Zanop Technologies Logo">
                    <h2>Zanop Technologies</h2>
                </a>
                <nav class="list">
                    <a href="/">Home</a>
                    <a href="about.html">About</a>
                    <a href="contact.html">Contact Us</a>
                    <a href="downloads.html">Downloads</a>
                    <a href="team.html">The Team</a>
                </nav>
            </header>
      `;
    const currentPage = location.pathname.split("/").pop() || "/";

    this.querySelectorAll("nav a").forEach((link) => {
      if (link.getAttribute("href") === currentPage) {
        link.setAttribute("aria-current", "page");
      }
    });
  }
}

customElements.define("site-navbar", SiteNavbar);
