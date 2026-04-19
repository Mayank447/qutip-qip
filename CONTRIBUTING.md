# Contributing to QuTiP-qip Development

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. Please make sure to [read the relevant sections](#table-of-contents) before making your contribution.

## Table of Contents

- [Contributing to Code](#contributing-to-code)
    - [Before you start](#before-you-start)
    - [Choose an issue to work on](#choose-an-issue-to-work-on)
    - [Assigning Issues](#assigning-issues)
    - [Development Workflow](#development-workflow)
    - [Code Review](#code-review)
- [Improving the Documentation](#improving-the-documentation)
    - [Fixing typos and errors](#fixing-typos-and-errors)
    - [Adding new sections or topics, Improving explanations and examples](#adding-new-sections-or-topics,-improving-explanations-and-examples)
    - [Adding/Updating tutorials](#addingupdating-new-tutorials)
- [AI Tools Usage Policy](#ai-tools-usage-policy)

## Contributing to Code

### Before you start
It is best to familiarize yourself with the project. You can start by reading the [documentation](https://qutip-qip.readthedocs.io/en/latest/) and trying out the examples provided in the [tutorials](https://qutip-qip.readthedocs.io/en/latest/tutorials_v5.html).

### Choose an issue to work on
QuTiP-qip uses the following labels to help non-maintainers find issues best suited to their interests and experience level:

- [good first issue](https://github.com/qutip/qutip-qip/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) - these issues are typically the simplest available to work on, ideal for newcomers. They should already be fully scoped, with a clear approach outlined in the descriptions.
- [help wanted](https://github.com/qutip/qutip-qip/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) - these issues are generally more complex than good first issues. They typically cover work that core maintainers don't currently have capacity to implement and may require more investigation/discussion. These are a great option for experienced contributors looking for something a bit more challenging.

### Assigning Issues
In our workflow, we generally avoid formally assigning issues to contributors. This approach is intentional — it keeps the project open and flexible, allowing anyone from the community to explore and work on problems that interest them, without waiting for explicit assignment or approval.

The only exception to this is a small subset of “core” issues. These are typically more complex, sensitive, or tightly coupled to ongoing development efforts, and are therefore handled directly by maintainers.

### Development Workflow
Please refer to the [contributing to code](https://qutip-qip.readthedocs.io/en/latest/contribution-code.html) section of the documentation for details on our development workflow, including how to set up the Python environment, style code, run tests and submit pull requests (PR).

You may also open a draft PR with changes in order to discuss and receive feedback on the best approach if you are not sure what the best way forward is.

### Code Review
Code review is done in the open and is open to anyone. While only maintainers have access to merge commits, community feedback on pull requests is extremely valuable. It is also a good mechanism to learn about the code base both for the contributor and reviewer.

Response times may vary for your PR due to other commitments the maintainers have. If you have been waiting over a week for a review on your PR feel free to tag the relevant maintainer in a comment to gently remind them to review your work.

<br>

## Contributing to Documentation
Thank you for your interest in improving our documentation! Clear, accurate, and well-structured documentation is essential for making this project accessible and useful to everyone. We welcome contributions of all sizes—from small typo fixes to entirely new sections.

### Setting up the environment
Please follow the instructions in the [contributing to documentation](https://qutip-qip.readthedocs.io/en/latest/contribution-docs.html) to build the documentation and to run the doctests locally.

### Fixing typos and errors
If you spot a typo, broken link, grammatical mistake, or notice any information in the documentation that is outdated or incorrect, feel free to open a Pull Request directly with your fixes. Every bit helps!

### Enhancing and Expanding Documentation
If you come across any section of the documentation that could be explained more clearly, have ideas for improving existing examples, or think a new section or topic would be beneficial, please open an issue first to discuss your suggestions. After the changes have been discussed and agreed upon, you can proceed to submit a Pull Request with your proposed updates.

### Tutorials
You can add new tutorials or update existing ones in the [Tutorials](http://github.com/qutip/qutip-tutorials/) repository. If you have an idea for a tutorial example that you think would be helpful to others, please feel free to submit a pull request with your suggested tutorial.

<br>

## AI Tools Usage Policy
We acknowledge the use of AI tools to improve efficiency and enhance quality of work. We only ask that the contributors follow the below guidelines:

### 1. Accountability

The human contributor is the solely responsible for their contribution i.e. all the AI-generated outputs can be considered their own work. If you're submitting a Pull Request that includes AI-generated code, documentation:

- You are responsible for ensuring that code you submit meets the qutip-qip project’s standards.
- You must fully understand every line of code in the submission.
- You must be able to explain the "why" behind the implementation during the review process.

### 2. Transparency

All Pull Requests must fill the "AI Tools Usage" section in the pull request template. This disclosure is mandatory and must reflect the actual use of AI tools.

### 3. Copyright & Legal

By submitting a contribution to qutip-qip, you agree to

1. Submit your contribution under the project's license and hold the copyright to your changes.

2. The contribution does not violate the terms of service of the AI Model/Tool provider and does not include "regurgitated" code from libraries with incompatible licenses (e.g., GPL-licensed code) being suggested into our BSD-3 licensed project.

3. AI agents must not sign commits or be added to commit message trailer `Co-authored-by:` since copyright is fundamentally tied to the concept of human authorship as per the Copyright law. You can instead use `Assisted-by: AI Model/Tool` as commit message trailer e.g. `Assisted-by: Claude Code with Opus 4.6`.

### 4. Prohibited Use

The following are strictly prohibited and will result in an immediate closure of the PR:

- **Ban on Bots/Agents:** Fully autonomous or unsupervised AI agents (e.g. OpenClaw etc.) are not allowed to submit pull requests.
- **Communication:** In communication whether via GitHub Issues/Discussion, writing PR desciptions or replying to comments, we expect to communicate directly with other humans not with automated systems. Use of translation tools is completely welcome.

### 5. Enforcement

Maintainers reserve the right to close any PR that appears to be a "low-effort" AI contribution.
