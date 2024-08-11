import argparse
from typing import Dict, Any, List, Tuple

from rich.console import Console
from rich.table import Table

from dmhylib import DmhySearch

console = Console()


def search_dmhy(search_params: Dict[str, Any]) -> Tuple[List[Dict[str, str]], DmhySearch]:
    """
    搜索动漫花园并返回结果列表和搜索器实例
    """
    try:
        searcher = DmhySearch(verify=False)
        searcher.search(**search_params)
        results = [{'Title': title, 'Size': size} for title, size in zip(searcher.titles, searcher.sizes)]
        return results, searcher
    except Exception as e:
        console.print(f"[bold red]搜索出错: {str(e)}[/bold red]")
        return [], None


def format_results(results: List[Dict[str, str]]) -> None:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("序号", style="dim", justify="right", width=4)
    table.add_column("标题", style="dim", width=60, overflow="fold")
    table.add_column("大小", justify="right", style="cyan", width=10)

    for idx, result in enumerate(results, start=1):
        table.add_row(str(idx), result['Title'], result['Size'])

    console.print(table)


def get_user_selection(max_num: int) -> int:
    while True:
        try:
            num = int(input("选择一个并输入其序号 (输入 0 退出): "))
            if 0 <= num <= max_num:
                return num
            else:
                console.print(f"[bold red]请输入 0 到 {max_num} 之间的数字[/bold red]")
        except ValueError:
            console.print("[bold red]请输入有效的数字[/bold red]")


def handle_search(args: argparse.Namespace) -> None:
    search_params = {'keyword': args.keyword}
    for param in ['sort_id', 'team_id', 'order']:
        if getattr(args, param) is not None:
            search_params[param] = getattr(args, param)

    results, searcher = search_dmhy(search_params)
    if results and searcher:
        format_results(results)
        selection = get_user_selection(searcher.sum)
        if selection > 0:
            num = selection - 1
            searcher.time = searcher.times[num]
            searcher.title = searcher.titles[num]
            searcher.size = searcher.sizes[num]
            searcher.magnet = searcher.magnets[num]

            console.print(f"[bold green]已选择 {searcher.title}[/bold green]")
            console.print(f"[bold green]其磁链为: [/bold green][bold yellow]{searcher.magnet}[/bold yellow]")
        else:
            console.print("[bold yellow]已退出选择[/bold yellow]")
    elif searcher is None:
        console.print("[bold red]搜索失败，无法进行选择[/bold red]")
    else:
        console.print("[bold yellow]搜索结果为空[/bold yellow]")


def main() -> None:
    parser = argparse.ArgumentParser(description="动漫花园搜索工具:")
    subparsers = parser.add_subparsers(dest='command')

    search = subparsers.add_parser('search',
                                   help='搜索动漫花园，不知道可用的参数请参阅dmhy.org的查询字符串'
                                   )
    search.add_argument('-k', '--keyword', type=str, help='搜索关键词', required=True)
    search.add_argument('-s', '--sort-id', type=int, help='搜索分类ID')
    search.add_argument('-t', '--team-id', type=int, help='发布团队ID')
    search.add_argument('-o', '--order', type=str, help='排序方式')

    args = parser.parse_args()

    if args.command == 'search':
        handle_search(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
