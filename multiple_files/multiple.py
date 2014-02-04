from pelican import signals


def initialize(pelican):
    if pelican:
        pelican.settings.setdefault('MULTIPLE_FILES_RENDER_META', 'render_multiple')
        pelican.settings.setdefault('MULTIPLE_FILES_OUTPUT_LIST', 'content_list')


def multiple_files(generator):
    file_marker = generator.settings['MULTIPLE_FILES_RENDER_META']
    list_name = generator.settings['MULTIPLE_FILES_OUTPUT_LIST']
    # list of articles which have the marker
    article_multi = []
    # index of articles in generator
    article_mulit_index = []
    # extract articles which have the marker set and get their index in the list
    for idx, article in enumerate(generator.articles):
        if hasattr(article, file_marker):
            article_multi.append(article)
            article_mulit_index.append(idx)

    # delete articles from generator
    for index in reversed(article_mulit_index):
        del(generator.articles[index])

    # get the save_as metadata
    save_url_list = extract_save_url(article_multi)

    # list of articles with content extracted from multiple files
    article_list = []
    for link in save_url_list:
        link_index = 0
        index = 1
        for article in article_multi:
            if article.save_as == link:
                temp_content = article.content
                if index == 1:
                    article_list.append(article)
                    setattr(article_list[link_index], list_name, [])
                    index += 1
                getattr(article_list[link_index], list_name).append(temp_content)

        link_index += 1

    # append the generated list to generator object
    for article in article_list:
        generator.articles.append(article)


def extract_save_url(article_list):
    save_link_list = []
    for article in article_list:
            if article.save_as not in save_link_list:
                save_link_list.append(article.save_as)
    return save_link_list


def register():
    signals.initialized.connect(initialize)
    signals.article_generator_finalized.connect(multiple_files)
