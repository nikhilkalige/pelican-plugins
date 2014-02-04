Render Multiple Files
===

**Author**: Nikhil Kalige

This plugins helps one push multiple articles to a single template


Settings
---
    # This sets the metadata that the plugin looks for in the articles
    MULTIPLE_FILES_RENDER_META: 'render_multiple'

    # This sets the name of list offered in the template
    MULTIPLE_FILES_OUTPUT_LIST: 'article_list'

For the plugin to work, **'render_multiple'** metadata should be set in the article. Besides that the files that need to be rendered as as single article should have same value set for **'save_as'** metadata in the articles

Content list is available in the template as a dictionary by the name **'article_list'**, with key set as title of the article.


