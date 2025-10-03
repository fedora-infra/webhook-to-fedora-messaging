export const ServiceTypes = {
  github: {
    name: "GitHub",
    title: "GitHub repositories",
    helpText: {
      name: "The full repository name, such as <tt>fedora-infra/bodhi</tt>",
      general:
        "Note that you can also add the webhook at the organization level, which will make it active for all the organization's repos. We suggest doing so to save some effort and automatically cover repos you may add in the future (make sure however than another teammate hasn't already added it).",
    },
  },
  gitlab: {
    name: "GitLab",
    title: "GitLab repositories",
    helpText: {
      name: "The full repository name, such as <tt>fedora-infra/bodhi</tt>",
      general:
        "Note that you can also add the webhook at the group level, which will make it active for all the group's repos. We suggest doing so to save some effort and automatically cover repos you may add in the future (make sure however than another teammate hasn't already added it).",
    },
  },
  forgejo: {
    name: "Forgejo",
    title: "Forgejo repositories",
    helpText: {
      name: "The instance and full repository name, such as <tt>codeberg.org/fedora-infra/bodhi</tt>",
      general:
        "Note that you can also add the webhook at the organization level, which will make it active for all the organization's repos. We suggest doing so to save some effort and automatically cover repos you may add in the future (make sure however than another teammate hasn't already added it).",
    },
  },
  discourse: {
    name: "Discourse",
    title: "Discourse forums",
    helpText: {
      name: "The name of the Discourse instance",
    },
  },
};

export const flawText = [
  "Flat tyre - You should be walking",
  "How about we explore the area ahead of us later?",
  "This is surely not what you were looking for",
  "I swear it was supposed to be here",
  "Segmentation fault - Core dumped",
  "Redirecting to SourceForge - Just kidding",
  "It is okay to get lost every now and then",
  "Even the things we love break sometimes",
  "Try refreshing and see if you find it?",
  "We looked everywhere - Even under the couch",
];
