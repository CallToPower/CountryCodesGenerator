import csv
import os
import logging
import time

SETTINGS = {
    'csv_delimiter': ',',
    'file': {
        'data_csv': 'data/country-codes.csv',
        'in_template_java': 'templates/CountryCodes.java',
        'out_java': 'out/CountryCodes.java'
    },
    'generator_name': os.path.basename(__file__),
    # Logging configuration
    'logging': {
        'loglevel': logging.INFO,
        'date_format': '%Y-%m-%d %H:%M:%S',
        'format': '[%(asctime)s] [%(levelname)-5s] [%(module)-20s:%(lineno)-4s] %(message)s'
    }
}


key_name = 'ISO3166-1-Alpha-2'
key_alpha2 = 'ISO3166-1-Alpha-2'
key_alpha3 = 'ISO3166-1-Alpha-3'
key_numeric = 'ISO3166-1-numeric'


def initialize_logger(loglevel, frmt, datefmt):
    '''Initializes the logger

    :param loglevel: The log level
    :param frmt: The log format
    :param datefmt: The date format
    '''
    logging.basicConfig(level=loglevel, format=frmt, datefmt=datefmt)


def parse_country_codes(filename, delimiter=','):
    '''Parses the country codes

    :param filename: The input data filename
    :return: The country codes object
    '''
    logging.info('Parsing country codes')
    country_codes = {}
    with open(filename, 'r', encoding='utf-8') as csvfile:
        logging.info('Reading from file "{}"'.format(filename))
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            country_codes[row[key_name]] = {
                key_alpha2: row[key_alpha2],
                key_alpha3: row[key_alpha3],
                key_numeric: row[key_numeric]
            }
    return country_codes


def generate_java_enum(country_codes, filename_template, generator_name='Generator'):
    '''Generates the Java Enumeration

    :param country_codes: The country codes
    :param filename_template: The filename template
    :return: The content of the Java Enumeration
    '''
    logging.info('Generating java enum')
    replacement = ''
    errors = []
    logging.info('Reading from template file "{}"'.format(filename_template))
    with open(filename_template, 'r', encoding='utf-8') as templatefile:
        template = templatefile.read()
    if template:
        first = True
        for country in country_codes:
            try:
                alpha2 = country_codes[country][key_alpha2]
                alpha3 = country_codes[country][key_alpha3]
                numeric = int(country_codes[country][key_numeric])
                if country and alpha2 and alpha3 and numeric:
                    replacement += '{}{}("{}", "{}", "{}", {}),\n'.format('' if first else '    ',
                                                                          alpha3, country, alpha2, alpha3, numeric)
                    first = False
            except ValueError as ve:
                errors.append({
                    'error': ve,
                    'country': country,
                    'alpha2': country_codes[country][key_alpha2],
                    'alpha3': country_codes[country][key_alpha3],
                    'numeric': country_codes[country][key_numeric]
                })
        replacement += '    ;'

        if errors:
            len_err = len(errors)
            logging.error('{} Error{} while processing data:'.format(
                len_err, 's' if len_err != 1 else ''))
            for c, error in enumerate(errors):
                logging.error('{} >>>> {}'.format(c + 1, error))

        logging.info('Replacing metadata in template')
        template = template.replace(
            '$GENERATOR_NAME$', SETTINGS['generator_name'])
        template = template.replace(
            '$GENERATION_DATE$', time.strftime("%Y-%m-%d %H:%M"))
        logging.info('Replacing enum values in template')
        template = template.replace('$ENUM_VALUES$', replacement)
        return template
    return ''


def write_java_file(filename, content):
    '''Writes to output file

    :param filename: The filename
    :param content: The content to be written
    '''
    logging.info('Writing java file')
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    elif os.path.isfile(filename):
        os.remove(filename)
    logging.info('Writing to file "{}"'.format(filename))
    with open(filename, 'w+', encoding='utf-8') as outfile:
        outfile.write(content)


if __name__ == '__main__':
    initialize_logger(SETTINGS['logging']['loglevel'], SETTINGS['logging']
                      ['format'], SETTINGS['logging']['date_format'])

    logging.info('Starting processing')
    country_codes = parse_country_codes(
        SETTINGS['file']['data_csv'], delimiter=SETTINGS['csv_delimiter'])
    java_file_content = generate_java_enum(
        country_codes, SETTINGS['file']['in_template_java'])
    write_java_file(SETTINGS['file']['out_java'], java_file_content)
    logging.info('Done')
