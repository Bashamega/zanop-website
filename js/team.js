const team = [
  {
    name: "Chirag Ruhil",
    role: "Head of Talent & Frontend Developer",
    bio: "Recruits people and codes our website.",
    avatar: "https://avatars.githubusercontent.com/u/314662218?s=96&v=4",
    avatarAlt: "Portrait of Chirag",
  },
  {
    name: "Adam Naji",
    role: "Project Manager & Full-Stack Developer",
    bio: "Leads project development, coordinates the team, and oversees frontend and backend implementation.",
    avatar: "https://avatars.githubusercontent.com/u/110662505?s=96&v=4",
    avatarAlt: "Portrait of Adam",
  },
  {
    name: "Gian",
    role: "Frontend Developer",
    bio: "Codes our frontend.",
    avatar: "https://avatars.githubusercontent.com/u/164229548?s=96&v=4",
    avatarAlt: "Portrait of Gian",
  },
  {
    name: "Ezraieel",
    role: "Kernel Developer",
    bio: "Develops our kernel.",
    avatar: "https://avatars.githubusercontent.com/u/80192196?s=96&v=4",
    avatarAlt: "Portrait of Ezraieel",
  },
  {
    name: "Greenvill",
    role: "Kernel Developer",
    bio: "Develops our kernel.",
    avatar: "https://avatars.githubusercontent.com/u/135178228?s=96&v=4",
    avatarAlt: "Portrait of Greenvill",
  },
  {
    name: "Morimura",
    role: "Kernel Developer",
    bio: "Develops our kernel.",
    avatar: "https://avatars.githubusercontent.com/u/217427055?v=4",
    avatarAlt: "Portrait of Morimura",
  },
  {
    name: "Hashes",
    role: "Applications and Development Tools",
    bio: "Develops applications",
    avatar: "https://avatars.githubusercontent.com/u/280577634?v=4",
    avatarAlt: "Portrait of Hashes",
  },
  {
    name: "Centolinho",
    role: "Frontend Project manager",
    bio: "Frontend dev",
    avatar: "https://avatars.githubusercontent.com/u/70218002?v=4",
    avatarAlt: "Portrait of Centolinho",
  },
];

const teamGrid = document.querySelector("#team-grid");
if (!teamGrid) {
  throw new Error("Team grid element was not found.");
}

for (const member of team) {
  const card = document.createElement("article");
  card.className = "team-card";

  const avatar = document.createElement("img");
  avatar.src = member.avatar;
  avatar.alt = member.avatarAlt;
  avatar.className = "team-avatar";

  const name = document.createElement("h3");
  name.textContent = member.name;
  name.className = "team-name";

  const role = document.createElement("p");
  role.textContent = member.role;
  role.className = "team-role";

  const bio = document.createElement("p");
  bio.textContent = member.bio;
  bio.className = "team-bio";

  card.append(avatar, name, role, bio);
  teamGrid.append(card);
}
