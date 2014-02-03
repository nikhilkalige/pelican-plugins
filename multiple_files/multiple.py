from pelican import signals


def initialize(pelican):
    if pelican:
        pelican.settings.setdefault('RENDER_MULTIPLE_FILES', 'RENDER_MULTIPLE')


def multiple_files(generator):
    file_marker = generator.settings['RENDER_MULTIPLE_FILES']
    article_multi = []
    article_mulit_index = []
    for idx, article in enumerate(generator.articles):
        if hasattr(article, 'multi'):
            article_multi.append(article)
            article_mulit_index.append(idx)

    #delete items from the generator which have multi set
    for index in reversed(article_mulit_index):
        del(generator.articles[index])

    save_url_list = extract_save_url(article_multi)

    article_list = []
    for link in save_url_list:
        link_index = 0
        index = 1
        for article in article_multi:
            if article.save_as == link:
                temp_content = article.content
                if index == 1:
                    article_list.append(article)
                    article_list[link_index].content_list = []
                    index += 1
                article_list[link_index].content_list.append(temp_content)
        link_index += 1

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
