Git Versioned Output
===

**Author**: Nikhil Kalige

This plugin generates output for version controlled pelican directory. It generates output at separate directory if content has been tagged.


Settings
---
    # this sets the name for directory which holds all plugin generated content
    GIT_VERSIONED_OUTPUT_LOCATION = version
    
    # this sets the directory name pattern for tags
    # it should contain {tag} inorder to be considered a valid value
    # ex: if git tag = a1 and setting is v-{tag}, output folder name will be v-a1
    GIT_VERSIONED_OUTPUT_TAG = v-{tag}
    
Behaviour
---

Plugin will generate output at tagged location under following circumstances
 * Folder is a git repository
 * Repository has no untracked files
 * Repository is clean
 * The commit currently pointed to by the repository is tagged

If the above conditions are not met, then output will be generated as pelican does it normally which is in output folder
