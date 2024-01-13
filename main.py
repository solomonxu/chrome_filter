import argparse
from proxy_filter import ProxyFilter

# Main Function
def main(input_url, pattern):
    try:
        # New a proxy filter
        filter = ProxyFilter()
        # Open browser and get source url from proxy log
        filtered_urls = filter.filterFileUrls(input_url, pattern)
    finally:
        # Cleanup
        filter.cleanup()
    
    # Output urls
    print("filtered urls: ")
    print(filtered_urls)

# Entry
if __name__ == '__main__':
    description = 'Helper script for downloading and trimming kinetics videos.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_url', type=str, default='input_url1',
                   help='Input url of page which video or big file included.')
    parser.add_argument('pattern', type=str, default='pattern1',
                   help='Pattern of source url which video or big file.')
    main(**vars(parser.parse_args()))
