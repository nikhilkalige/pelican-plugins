from pelican import signals

def initialized(pelican):
    print("Plugin initialized")


#def metadata_check(instance):
def metadata_check(generator):
    print("Metadata function running")
    article_multi = []
    article_mulit_index = []
    for idx, article in enumerate(generator.articles):
        if hasattr(article, 'multi'):
            article_multi.append(article)
            article_mulit_index.append(idx)
        else:
            print("Absent")

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

    print("Finished running")


def extract_save_url(article_list):
    save_link_list = []
    for article in article_list:
            if article.save_as not in save_link_list:
                save_link_list.append(article.save_as)
    return save_link_list


def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(metadata_check)
