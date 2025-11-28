from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.tree import Tree

from agent import Agent
from tools import tools_map

def main():
    load_dotenv()
    console = Console()
    
    agent = Agent(model="gemini-3-pro-preview", tools=tools_map)
    
    console.print(Panel.fit("File Manager Agent", style="bold blue"))
    console.print("Type [bold red]exit[/bold red] to quit.\n")

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
            if user_input.lower() == "exit":
                break
            
            agent.clear_trace()
            with console.status("[bold yellow]Generating output...[/bold yellow]", spinner="dots"):
                response = agent.run(contents=user_input)
            
            if agent.trace:
                tree = Tree("Execution Trace")
                for step in agent.trace:
                    func_node = tree.add(f"[bold cyan]{step['name']}[/bold cyan]")
                    func_node.add(f"Args: {step['args']}")
                    func_node.add(f"Result: {step['result']}")
                console.print(tree)
                console.print()

            if isinstance(response, str):
                console.print(f"[bold red]Agent Error:[/bold red] {response}")
            elif hasattr(response, "text"):
                console.print(Panel(Markdown(response.text), title="Agent", border_style="green"))
            else:
                console.print(f"[bold red]Unexpected response type:[/bold red] {type(response)}")

        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"\n[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
