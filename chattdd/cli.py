import click
from chattdd.core import initialize_model, generate_function
from chattdd.file_handler import write_to_file


@click.group()
def cli():
    pass


def generate_and_save(description_str, save_function_code=True):
    click.echo(f"Generating code for: {description_str}")

    # Initialize Langchain model
    model = initialize_model()

    # Invoke langchain model
    try:
        output_json = generate_function(model, description_str)
    except Exception as e:
        click.echo(f"Error: {e}")
        return

    # Interpret results
    function_name = output_json['function_name']
    function_code = output_json['function_code']
    function_file_name = output_json['function_file_name']
    test_code = output_json['test_code']
    test_file_name = output_json['test_file_name']

    # Write to files
    write_to_file(test_code, f'tests/{test_file_name}')
    if save_function_code:
        write_to_file(function_code, f'src/{function_file_name}')

    click.echo(f"Generated function: {function_name}")


@cli.command()
@click.argument('description', nargs=-1)
def test_and_code(description):
    description_str = ' '.join(description)
    generate_and_save(description_str)


@cli.command()
@click.argument('description', nargs=-1)
def test(description):
    description_str = ' '.join(description)
    generate_and_save(description_str, save_function_code=False)


if __name__ == "__main__":
    cli()