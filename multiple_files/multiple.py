from pelican import signals
from pelican.utils import slugify


def multiple_articles(generator):
    multiple_files(generator, 'articles')


def multiple_pages(generator):
    multiple_files(generator, 'pages')


def multiple_files(generator, file_class):
    file_marker = generator.settings.get('MULTIPLE_FILES_RENDER_META', 'render_multiple')
    list_name = generator.settings.get('MULTIPLE_FILES_OUTPUT_LIST', 'article_list')

    # list of files which have the marker
    file_multi = [article for article in getattr(generator, file_class) if hasattr(article, file_marker)]

    # delete files from generator
    for article in file_multi:
        getattr(generator, file_class).remove(article)

    # get the save_as metadata
    save_url_list = extract_save_url(file_multi)

    # list of files with content extracted from multiple files
    file_list = []
    for link in save_url_list:
        link_index = 0
        index = 1
        for article in file_multi:
            if article.override_save_as == link:
                temp_title = slugify(article.title)
                if index == 1:
                    file_list.append(article)
                    setattr(file_list[link_index], list_name, dict())
                    index += 1
                getattr(file_list[link_index], list_name)[temp_title] = article
        link_index += 1

    # append the generated list to generator object
    for article in file_list:
        getattr(generator, file_class).append(article)
    print("")


def extract_save_url(file_list):
    save_link_list = []
    for article in file_list:
            if article.override_save_as not in save_link_list:
                save_link_list.append(article.override_save_as)
    #save_link_list = [article.override_save_as for article in file_list if article.override_save_as not in save_link_list]
    return save_link_list


def register():
    signals.article_generator_finalized.connect(multiple_articles)
    signals.page_generator_finalized.connect(multiple_pages)
