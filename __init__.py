from opsdroid.matchers import match_regex
import logging

@match_regex(r'help$')
async def help(opsdroid, config, message):
    """help - Displays this help message"""
    response = []
    for skill in opsdroid.skills:
        if skill.__doc__:
            response.append("{}: {}".format(skill.__name__, skill.__doc__))
        else:
            logging.debug('doc string not found for {}'.format(skill.__name__))
            response.append(skill.__name__)
    await message.respond('\n'.join(sorted(response)))

@match_regex(r'help (.*)')
async def help_skill(opsdroid, config, message):
    """help <skill_name> - Displays usage for provided skill"""
    logging.debug("searching for {}".format(message.regex))
    found_skill = next((skill for skill in opsdroid.skills if skill.__name__ == message.regex.group(1)), False)
    if not found_skill:
        response = "{} skill not found".format(message.regex.group(1))
    elif not found_skill.__doc__:
        response = "No usage found for {}".format(found_skill.__name__)
    else:
        response = found_skill.__doc__
    await message.respond(response)
