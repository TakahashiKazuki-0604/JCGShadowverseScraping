# -*- coding: utf-8 -*-
import jcg_scraping
import setting

driver = jcg_scraping.init()
jcg_scraping.move_page(driver,setting.URL)
jcg_scraping.jcg_entry_page_get(driver)
class_urls = jcg_scraping.jcg_class_urls_parser(driver)
card_dictionary = jcg_scraping.get_card_dictionary(driver,class_urls)
class_dictionary = jcg_scraping.jcg_class_counter(class_urls)
jcg_scraping.close(driver)
jcg_scraping.print_card_dictionary(card_dictionary)
jcg_scraping.print_class_dictionary(class_dictionary)
jcg_scraping.print_card_csv(card_dictionary,class_dictionary)
