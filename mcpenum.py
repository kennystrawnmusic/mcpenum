import asyncio
import argparse

from fastmcp import Client, FastMCP

async def main_inner(args):

    base_url = args.url.rstrip('/')
    endpoint = args.endpoint.lstrip('/')
    url = f"{base_url}/{endpoint}"

    client = Client(url, auth=args.auth) if args.auth else Client(url)

    async with client:
        await client.ping()

        prompts = await client.list_prompts()
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
        tools = await client.list_tools()

        print("Prompts:")
        for prompt in prompts:
            print('***')
            print(prompt.name)
            print(prompt.description.strip())

        print("Resources:")
        for resource in resources:
            print('***')
            print(resource.name)
            print(resource.description.strip())

        print("-"*50)
        print("Resource Templates:")
        for resource_template in resource_templates:
            print('***')
            print(resource_template.uriTemplate)
            print(resource_template.description.strip())

        print("-"*50)
        print("Tools:")
        for tool in tools:
            print('***')
            params = list(tool.inputSchema.get('properties').keys())
            print(f"{tool.name}({','.join(params)})")
            print(tool.description.strip())

def main():
    parser = argparse.ArgumentParser(description="MCP enumeration tool.")

    parser.add_argument('--url', required=True, type=str, help="MCP server URL")
    parser.add_argument('--endpoint', required=True, type=str, help="MCP endpoint")
    parser.add_argument('--auth', type=str, help="MCP authentication mechanism")

    args = parser.parse_args()

    asyncio.run(main_inner(args))

if __name__ == '__main__':
    main()