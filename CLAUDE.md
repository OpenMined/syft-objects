Whenever you make changes to any files:
- Commit your code in that project's git repo with an insightful commit message.
- Run unit tests for that project to make sure we haven't broken anything
- every time you make a change, update the version by a minor version. For example, if the version was 3.5.3, when you make a commit update it to 3.5.4 (this helps me know whether the changes are actually amking their way to the jupyter notebook where i'm doing manual testing). Don't forget to update __verion__.

When it seems like we've solved a problem: 
- Look back in the recent history of commits and in the context window, and use the context to write a unit test

Packaging:
- when you need to run "python" use uv instead.

Testing:
- don't stop writing tests until you reach 100% code coverage
- if you're writing tests in syft-queue, don't forget to prefix queues with "test_Q:" and jobs with "test_J:" instead of the normal "Q:" and "J:" respectively