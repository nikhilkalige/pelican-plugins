Render Multiple Files
===

**Author**: Nikhil Kalige

This plugins helps one push multiple articles to a single template


Settings
---
    # This sets the metadata that the plugin looks for in the articles
    MULTIPLE_FILES_RENDER_META: 'RENDER_MULTIPLE'

    # This sets the name of list offered in the template
    MULTIPLE_FILES_OUTPUT_LIST: 'content_list'

For the plugin to work, 'RENDER_MULTIPLE' metadata should be set in the article. Besides that the files that need to be rendered as as single article should have same value set for 'save_as' metadata in the articles


