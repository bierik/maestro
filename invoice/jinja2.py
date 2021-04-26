from jinja2 import Environment

"""
Custom jinja2 environment for latex file processing.
"""


def environment(**options):
    return Environment(
        loader=options["loader"],
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
    )
