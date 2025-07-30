import time
import create_rtree

def load_dataset(filepath):
    # Loads data points from a specified file, 
    # storing each entry as a dictionary with 'id', 'x', and 'y' values.
    points = []  # Initialize an empty list to hold data points
    with open(filepath, 'r') as file:  # Open the file for reading
        for line in file:  # Iterate through each line in the file
            data = line.strip().split()  # Remove whitespace and split the line into components
            point = {'id': data[0], 'x': float(data[1]), 'y': float(data[2])}  # Create a dictionary for the point
            points.append(point)  # Add the point to the list
    return points  # Return the list of points


def sequential_skyline(datasets):
    # Performs a skyline computation using a sequential scan across the datasets provided.
    all_points = []  # Initialize an empty list to hold all points from all datasets
    for dataset in datasets:  # Iterate through each dataset
        all_points.extend(load_dataset(dataset))  # Load points from the dataset and add them to all_points

    skyline = []  # Initialize an empty list to hold skyline points
    for point in all_points:  # Iterate through each point in all_points
        # Check if the current point is not dominated by any other point
        if not any(is_dominated_by(other, point) for other in all_points):
            skyline.append(point)  # If not dominated, add to skyline

    # Ensure unique skyline points and sort by 'x' ascending and 'y' descending
    unique_skyline_points = {p['id']: p for p in skyline}.values()
    return sorted(unique_skyline_points, key=lambda p: (p['x'], -p['y']))  # Return sorted unique skyline points


def minimum_distance(mbr):
    # Calculates distance from the origin to the MBR considering only its lowest cost and highest area values.
    return mbr['x1']**2 + mbr['y2']**2


def bbs_skyline(rtree):
    # Executes the Branch-and-Bound Skyline algorithm using the provided R-tree to extract skyline points.
    skyline = []
    candidates = [(minimum_distance(rtree.root.MBR), rtree.root)]
    candidates.sort(key=lambda x: x[0])

    while candidates:  
        _, node = candidates.pop(0)  # Get the node with the smallest distance

        if node.is_leaf():  # If the node is a leaf
            for point in node.data_points:  # Iterate through each data point in the leaf node
                # Check if the point is not dominated by any skyline point
                if not any(is_dominated_by(sky_point, point) for sky_point in skyline):
                    # Remove points from skyline that are dominated by the current point
                    skyline = [sky_point for sky_point in skyline if not is_dominated_by(point, sky_point)]
                    skyline.append(point)  # Add the current point to skyline
        else:  # If the node is not a leaf
            for child in node.child_nodes:  # Iterate through child nodes
                child_mbr = {'x': child.MBR['x1'], 'y': child.MBR['y2']}  # Get the MBR of the child
                # Check if the child's MBR is not dominated by any skyline point
                if not any(is_dominated_by(sky_point, child_mbr) for sky_point in skyline):
                    candidates.append((minimum_distance(child.MBR), child))  # Add the child to candidates
            candidates.sort(key=lambda x: x[0])  # Sort candidates by minimum distance

    return skyline

def is_dominated_by(a, b):
    # Checks if point 'a' is dominated by point 'b' based on lower cost and higher area requirements.
    return a['x'] <= b['x'] and a['y'] >= b['y'] and (a['x'] < b['x'] or a['y'] > b['y'])


def split_dataset(points, dimension='x'):
    # Splits the dataset into two parts based on the median value of the specified dimension.
    sorted_points = sorted(points, key=lambda p: p[dimension])
    mid = len(sorted_points) // 2
    return sorted_points[:mid], sorted_points[mid:]


def bbs_divide_and_conquer(points):
    # Applies BBS using a divide-and-conquer approach by splitting the dataset and combining skyline results.
    subspace1, subspace2 = split_dataset(points)
    rtree1 = create_rtree.main(subspace1)
    rtree2 = create_rtree.main(subspace2)

    skyline1 = bbs_skyline(rtree1)
    skyline2 = bbs_skyline(rtree2)
    combined_skyline = skyline1 + skyline2

    final_skyline = []
    for point in combined_skyline:
        if not any(is_dominated_by(other, point) for other in combined_skyline):
            final_skyline.append(point)

    return final_skyline

def main():
    # Executes skyline algorithms and outputs results for sequential scan, BBS, and divide-and-conquer methods.
    dataset_path = "/Users/mdsarfuddinsabbir/Downloads/Assignment 2 Datasets/Task2_Datasets/city2.txt"  # Path to the dataset file
    with open('output_city2.txt', 'w') as output_file:  # Open output file for writing results
        points = load_dataset(dataset_path)  # Load points from the dataset

        start = time.time()  # Start timer for sequential skyline computation
        skyline_points = sequential_skyline([dataset_path])  # Compute skyline points sequentially
        output_file.write("Sequential Skyline Results:\n")  # Write header for sequential results
        for point in skyline_points:  # Iterate through skyline points
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")  # Write each point to the output file
        output_file.write(f"Sequential Execution Time: {time.time() - start}\n\n")  # Write execution time

        rtree = create_rtree.main(points)  # Create an R-tree for all points
        start = time.time()  # Start timer for BBS skyline computation
        bbs_points = bbs_skyline(rtree)  # Compute skyline points using BBS
        output_file.write("BBS Skyline Results:\n")  # Write header for BBS results
        for point in bbs_points:  # Iterate through BBS skyline points
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")  # Write each point to the output file
        output_file.write(f"BBS Execution Time: {time.time() - start}\n\n")  # Write execution time

        start = time.time()  # Start timer for divide-and-conquer skyline computation
        final_skyline = bbs_divide_and_conquer(points)  # Compute skyline points using divide-and-conquer
        output_file.write("Divide-and-Conquer Skyline Results:\n")  # Write header for divide-and-conquer results
        for point in final_skyline:  # Iterate through final skyline points
            output_file.write(f"{point['id']} {point['x']} {point['y']}\n")  # Write each point to the output file
        output_file.write(f"Divide-and-Conquer Execution Time: {time.time() - start}\n")  # Write execution time


if __name__ == "__main__":
    main()



