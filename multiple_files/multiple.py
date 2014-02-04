from pelican import signals
from pelican.utils import slugify


def initialize(pelican):
    if pelican:
        pelican.settings.setdefault('MULTIPLE_FILES_RENDER_META', 'render_multiple')
        pelican.settings.setdefault('MULTIPLE_FILES_OUTPUT_LIST', 'content_list')


def multiple_articles(generator):
    multiple_files(generator, 'articles')


def multiple_pages(generator):
    multiple_files(generator, 'pages')


def multiple_files(generator, file_class):
    file_marker = generator.settings['MULTIPLE_FILES_RENDER_META']
    list_name = generator.settings['MULTIPLE_FILES_OUTPUT_LIST']
    # list of files which have the marker
    file_multi = []
    # index of files in generator
    file_mulit_index = []
    # extract files which have the marker set and get their index in the list
    for idx, article in enumerate(getattr(generator, file_class)):
        if hasattr(article, file_marker):
            file_multi.append(article)
            file_mulit_index.append(idx)

    # delete files from generator
    for index in reversed(file_mulit_index):
        del(getattr(generator, file_class)[index])

    # get the save_as metadata
    save_url_list = extract_save_url(file_multi)

    # list of files with content extracted from multiple files
    file_list = []
    for link in save_url_list:
        link_index = 0
        index = 1
        for article in file_multi:
            if article.save_as == link:
                temp_content = article.content
                temp_title = slugify(article.title)
                if index == 1:
                    file_list.append(article)
                    setattr(file_list[link_index], list_name, dict())
                    index += 1
                getattr(file_list[link_index], list_name)[temp_title] = temp_content

        link_index += 1

    # append the generated list to generator object
    for article in file_list:
        getattr(generator, file_class).append(article)


def extract_save_url(file_list):
    save_link_list = []
    for article in file_list:
            if article.save_as not in save_link_list:
                save_link_list.append(article.save_as)
    return save_link_list


def register():
    signals.initialized.connect(initialize)
    signals.article_generator_finalized.connect(multiple_articles)
    signals.page_generator_finalized.connect(multiple_pages)
