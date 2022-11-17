from scraper import Scraper

if __name__ == '__main__':
    bot = Scraper()
    bot.close_pop_up()
    bot.create_dictionary()
    bot.extract_text_from_links()
    bot.extract_clefts_from_text()
    bot.save_data_to_json()
    bot.export_data_to_excel()