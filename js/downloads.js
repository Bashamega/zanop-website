const releases = [
  {
    version: "v0.2 Chicago",
    description: "The second Public Developer Release of Zanop Desktop OS.",
    url: "https://github.com/Zanop-Technologies/zanop-desktop-os/releases/tag/v0.2-alpha",
    latest: true,
  },
  {
    version: "v0.1 Chicago",
    description: "The first Public Developer Release of Zanop Desktop OS.",
    url: "https://github.com/Zanop-Technologies/zanop-desktop-os/releases/tag/v0.1-alpha",
    latest: false,
  },
];

const releaseList = document.querySelector("#release-list");
if (!releaseList) {
  throw new Error("Release list element was not found.");
}

for (const release of releases) {
  const card = document.createElement("article");
  card.classList.add("release-card", "glass");
  if (release.latest) {
    card.classList.add("latest");
  }

  const status = document.createElement("p");
  status.className = "release-status";
  status.textContent = release.latest ? "Latest release" : "Previous release";

  const title = document.createElement("h2");
  title.textContent = release.version;

  const description = document.createElement("p");
  description.className = "release-description";
  description.textContent = release.description;

  const link = document.createElement("a");
  link.className = "release-link";
  link.href = release.url;
  link.textContent = "View release on GitHub";

  card.append(status, title, description, link);
  releaseList.append(card);
}
