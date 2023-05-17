def get_regions():
    regions = []
    try:
        with open('regions.txt', 'r') as file:
            lines = file.readlines()
        regions = [line.strip().split(', ') for line in lines]
        print(f"Regions: {regions}")
    except FileNotFoundError:
        print("FileNotFoundError: The 'regions.txt' file was not found.")
    except Exception as e:
        print(f"Error reading 'regions.txt': {e}")
    return regions