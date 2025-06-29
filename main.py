import sys
from pathlib import Path

from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from prompt_toolkit.shortcuts import radiolist_dialog
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()
console = Console()

sample_texts = [
    "I love sunny days",
    "This is the worst movie I’ve ever seen",
    "It’s an okay product, nothing special"
]

def analyze_sentence(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)['compound']
    if score > 0.05:
        return 'positive'
    if score < -0.05:
        return 'negative'
    return 'neutral'

def run_demo():
    console.clear()
    console.rule("[bold yellow] Demo Sentiment Analysis [/]", style="magenta")
    table = Table(title="Sample Sentences", box=box.SIMPLE)
    table.add_column("Sentence", style="cyan")
    table.add_column("Sentiment", style="magenta")
    for s in sample_texts:
        table.add_row(s, analyze_sentence(s))
    console.print(table)
    console.print()
    input("Press [bold green]Enter[/] to return to menu…")

def run_text():
    console.clear()
    console.rule("[bold yellow] Single Sentence Analysis [/]", style="magenta")
    sentence = console.input("[bold cyan]Enter your sentence:[/] ")
    result = analyze_sentence(sentence)
    emoji = "😊" if result=='positive' else "😠" if result=='negative' else "😐"
    color = "green" if result=='positive' else "red" if result=='negative' else "yellow"
    console.print(f"\n[bold]{sentence}[/] → [{color}]{result.upper()}[/] {emoji}\n")
    input("Press [bold green]Enter[/] to return to menu…")

def run_file():
    console.clear()
    console.rule("[bold yellow] File Analysis [/]", style="magenta")
    path_str = console.input("[bold cyan]Enter path to text file:[/] ")
    path = Path(path_str)
    if not path.exists() or not path.is_file():
        console.print("[bold red]File not found or invalid path![/]\n")
        input("Press [bold green]Enter[/] to return to menu…")
        return

    lines = path.read_text(encoding='utf-8').splitlines()
    table = Table(title=f"Analysis of {path.name}", box=box.ROUNDED)
    table.add_column("Line", style="cyan", no_wrap=True)
    table.add_column("Sentiment", style="magenta")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        table.add_row(line, analyze_sentence(line))
    console.print(table)
    console.print()
    input("Press [bold green]Enter[/] to return to menu…")

def main():
    while True:
        choice = radiolist_dialog(
            title="🌈 Sentiment Analyzer",
            text="Select an option:",
            values=[
                ("demo",      "📊 Run Demo Analysis"),
                ("text",      "✍️  Analyze a Single Sentence"),
                ("file",      "📁 Analyze a Text File"),
                ("exit",      "❌ Exit"),
            ],
            style=None,
        ).run()

        if choice == "demo":
            run_demo()
        elif choice == "text":
            run_text()
        elif choice == "file":
            run_file()
        else:
            console.clear()
            console.print(Panel.fit("[bold red]Goodbye![/] 👋", style="yellow"))
            sys.exit()

if __name__ == "__main__":
    main()
