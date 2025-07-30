
import create_rtree
import math
import time

# Read query points from a file and store them
def main():
    """
    This function executes when the main.py file is run. The main objective of this function is to use the points from parking_dataset.txt 
    and query_points.txt files to execute the sequential_search, best_first_search, and divide_and_conquer function. 
    The coordinates from parking dataset are store in "points_list" where each is a dictionary with id, x coordinate value and y coordinate value. 
    Similarly, the coordinates from query_points are saved in "quesries" list.
    """

    points_list = [] #list to store all the coordinates from parking_dataset
    with open("parking_dataset.txt", 'r') as dataset:
        for data in dataset.readlines(): #readlines gets one line at every iteration
            data = data.split()  #split based on space to separate values of id, x, and y
            points_list.append({ #extract values from data and append them to points_list
                'id': int(data[0]),
                'x': float(data[1]),
                'y': float(data[2])
            })
            
    queries = [] #list to store all query coordinates
    #the process followed is exactly similar to above section
    with open("query_points.txt", 'r') as dataset:
        for data in dataset.readlines():
            data = data.split()
            point = {
                'id': int(data[0]),
                'x': float(data[1]),
                'y': float(data[2])
            }
            queries.append(point)


    #trigger the sequential search, best first search andd divide and conquer. Their respective functions contain all operations
    ss_time = sequential_search(points_list, queries) 
    bfs_time = best_first_search(points_list, queries)
    dcs_time = divide_and_conquer(points_list, queries)

    print("\nSummary of time taken of each search:")

    print(f"Total time taken for sequential search: {ss_time}")
    print(f"Average time taken for sequential search: {ss_time/len(queries)}\n")

    print(f"Total taken for best first search: {bfs_time}")
    print(f"Average time taken for best first search: {bfs_time/len(queries)}\n")

    print(f"Total taken for divide and conquer: {dcs_time}")
    print(f"Average time taken for divide and conquer: {dcs_time/len(queries)}\n")


def divide_and_conquer(points_list, queries):
    """
    Implements a divide and conquer approach to spatial querying by splitting the points into two subgroups, creating an R-tree for each, 
    and performing a Best-First Search (BFS) on each tree independently for each query. 

    Args:
    points_list (list of dicts): A list of dictionaries where each dictionary represents a point with its 'id', 'x', and 'y' coordinates.
    queries (list of dicts): A list of dictionaries representing the query points, with each dictionary containing 'id', 'x', and 'y' coordinates.

    Output:
    Writes the results to 'divide_and_conquer_output.txt', recording the closest point's 'id', 'x', and 'y' coordinates for each query.

    Performance:
    Measures the time taken for searching across both subtrees and prints it, providing insight into the method's efficiency.
    """

    points_list = sorted(points_list, key = lambda x: x['x']) #sorting based on x axis 

    #based on x axis data has been seperated into left and right from mid_point
    mid_point = len(points_list)//2
    left = points_list[:mid_point]
    right = points_list[mid_point:]

    print("\nIntiating RTree construction for divide and conquer....")
    #create r-tree for each segration
    left_rtree = create_rtree.main(left) 
    right_rtree = create_rtree.main(right)

    #starting time of the search
    checkpoint1_time = time.time()
    mindist_points = {}  # Dictionary to store results of closest points

    print("results of divide and conquer")
    for query in queries: #get search result for each query
        left_bfs_parking = BFS() #BFS object, this object will contain the nearest neighbor and the distance
        #mindist_mbrs attribute holds the distance between point and MBRs. Starting from distance = 0 and first MBR = root node
        left_bfs_parking.mindist_mbrs.append([0, left_rtree.root]) 
        left_bfs_parking.query = query #add the current quer yas parameter
        tree_traversal(left_bfs_parking, left_rtree.root) #get nearest neighbor for left section of data
        
        #following the same process as left section
        right_bfs_parking = BFS()
        right_bfs_parking.mindist_mbrs.append([0, right_rtree.root])
        right_bfs_parking.query = query
        tree_traversal(right_bfs_parking, right_rtree.root)

        #for this query final nearest neighbor from two nearest neighbors found doing tree_traversal for left and right section
        if left_bfs_parking.mindist_point[0] <= right_bfs_parking.mindist_point[0]:
            mindist_points[query['id']] = left_bfs_parking.mindist_point[1] #final NNS for this query
        else:
            mindist_points[query['id']] = right_bfs_parking.mindist_point[1] #final NNS for this query

        print(f"id = {mindist_points[query['id']]['id']}, x = {mindist_points[query['id']]['x']}, y = {mindist_points[query['id']]['y']} for query {query['id']}")

    #calculate the time taken for divide and conquer search of all 200 queries
    checkpoint2_time = time.time() 
    print("Total time taken for divide and conquer: ", checkpoint2_time - checkpoint1_time)

    #write the output in a txt file with time taken
    with open('divide_and_conquer_output.txt', 'w') as file:
        file.write(f"Total time taken for divide and conquer: {checkpoint2_time - checkpoint1_time}\n")
        file.write(f"Average time taken for divide and conquer: {(checkpoint2_time - checkpoint1_time)/len(queries)}\n\n")

        for query_id, query_result in mindist_points.items():
            id = query_result['id']
            x = query_result['x']
            y = query_result['y']
            file.write(f"id = {id}, x = {x}, y = {y} for query {query_id}\n")

    return checkpoint2_time - checkpoint1_time
    

def sequential_search(points_list, queries):
    """
    Performs a sequential search to find the nearest point for each query by directly comparing the Euclidean distance between each query 
    point and all points in the points list. This function serves as a baseline comparison to Best-First Search and Divide and Conquer.

    Args:
    points_list (list of dicts): A list of dictionaries where each dictionary represents a point with its 'id', 'x', and 'y' coordinates.
    queries (list of dicts): A list of dictionaries representing the query points, with each dictionary containing 'id', 'x', and 'y' coordinates.

    Output:
    Writes the results to 'sequential_output.txt', recording the closest point's 'id', 'x', and 'y' coordinates for each query.

    Performance:
    Measures the time taken for the sequential search and prints it, providing insight into the method's efficiency. This helps to gauge 
    the performance trade-offs when comparing to more sophisticated spatial querying techniques.
    """
    print("Results of sequential search: ")
    # Record the start time to measure the duration of the search process
    checkpoint1_time = time.time()
    query_results = {} # Dictionary to store the closest point for each query
    for query in queries: # Iterate over each query point
        distance_points = [] # List to hold distances between the query point and each point in the list
        # Calculate the distance from the query to each point in the list
        for point in points_list:
            # Compute the Euclidean distance between the current point and the query
            distance = euclidean_distance(point, query)
            # Store the calculated distance and the corresponding point
            distance_points.append([distance, point])
        
        # Find the point with the smallest distance to the query
        nearest_point = min(distance_points, key = lambda x: x[0])
        # Store the nearest point's details in the results dictionary using the query's id as the key
        query_results[query['id']] = nearest_point[1]
        print(f"id = {nearest_point[1]['id']}, x = {nearest_point[1]['x']}, y = {nearest_point[1]['y']} for query {query['id']}")

    # Record the end time to measure the duration of the search process
    checkpoint2_time = time.time()
    # Print the total time taken for the sequential search
    print("Total time taken for sequntial search: ", checkpoint2_time - checkpoint1_time)

    # Write the search results to a file
    with open('sequential_output.txt', 'w') as file:
        file.write(f"Total time taken for sequential search: {checkpoint2_time - checkpoint1_time}\n")
        file.write(f"Average time taken for sequential search: {(checkpoint2_time - checkpoint1_time)/len(queries)}\n\n")
        # Extract the id, x, and y coordinates of the nearest point
        for query_id, query_result in query_results.items():
            id = query_result['id']
            x = query_result['x']
            y = query_result['y']
            # Write the results to the file in the specified format
            file.write(f"id = {id}, x = {x}, y = {y} for query {query_id}\n")

    return checkpoint2_time - checkpoint1_time


def best_first_search(points_list, queries):
    """
    Executes the Best-First Search (BFS) algorithm using an R-tree constructed from the given points list. This is the function which prepares
    data - 
    * creating R-tree based on the points_list using the script in create_rtree.py file
    * creating bfs_parking object using the class BFS, which is later on used to store the nearest neighbors for each query and MBRs to be 
    traversed in the next iteration.

    Args:
    points_list (list of dicts): A list of dictionaries where each dictionary represents a point with its 'id', 'x', and 'y' coordinates.
    queries (list of dicts): A list of dictionaries representing the query points, with each dictionary containing 'id', 'x', and 'y' coordinates.

    Output:
    Writes the results of the search to 'output_bfs.txt', which includes the closest point's 'id', 'x', and 'y' coordinates for each query.

    Performance:
    The function measures the time taken to execute the BFS and prints it, providing insight into the algorithm's efficiency.
    """

    # Main function to run the best first search using an R-tree
    mindist_points = {}  # Dictionary to store results of closest points

    print("\nIntiating RTree construction for best first search....")
    rtree = create_rtree.main(points_list)  # Initialize the R-tree

    print("results of best first search")
    checkpoint1_time = time.time()
    for query in queries:
        bfs_parking = BFS()
        bfs_parking.mindist_mbrs.append([0, rtree.root])

        bfs_parking.query = query
        tree_traversal(bfs_parking, rtree.root)
        mindist_points[query['id']] = bfs_parking.mindist_point[1]
        print(f"id = {bfs_parking.mindist_point[1]['id']}, x = {bfs_parking.mindist_point[1]['x']}, y = {bfs_parking.mindist_point[1]['y']} for query {query['id']}")

    checkpoint2_time = time.time()
    print("Total time taken for best first search: ", checkpoint2_time - checkpoint1_time)

    # Write results to an output file
    with open('best_first_output.txt', 'w') as file:
        file.write(f"Total time taken for best first search: {checkpoint2_time - checkpoint1_time}\n")
        file.write(f"Average time taken for best first search: {(checkpoint2_time - checkpoint1_time)/len(queries)}\n\n")
        for query_id, query_result in mindist_points.items():
            id = query_result['id']
            x = query_result['x']
            y = query_result['y']
            file.write(f"id = {id}, x = {x}, y = {y} for query {query_id}\n")

    return checkpoint2_time - checkpoint1_time


class BFS:
    """
    A class representing the state and functionality of a Best-First Search (BFS) algorithm for spatial querying within an R-tree. This 
    class encapsulates the properties necessary to maintain the state of the search, including the minimum distance leaf node, a list of 
    minimum bounding rectangles (MBRs) with their distances, the query point, and the closest point found so far. It is designed to 
    efficiently determine the nearest neighbor to a given query point by exploring the R-tree nodes based on their proximity.

    Attributes:
    min_leaf_node (tuple or None): Stores the leaf node with the minimum distance found during the search, initially None.
    mindist_mbrs (list of tuples): A list where each tuple contains a distance to an MBR and the corresponding MBR node, used to prioritize 
    node traversal.
    query (dict): A dictionary containing the coordinates ('x', 'y') of the query point being searched.
    mindist_point (tuple or None): A tuple storing the closest point found and its distance from the query point, initially None.
    """

    def __init__(self):
        # Initialize properties to store the minimum leaf node, list of minimum distances to MBRs, query point, and closest point
        self.min_leaf_node = None
        self.mindist_mbrs = []  # List of tuples storing distance and corresponding MBR
        self.query = {}  # Dictionary to store query point coordinates
        self.mindist_point = None  # Tuple storing minimum distance and closest point found

def mindist_point_to_MBR(mbr_coord, query):
    """
    Calculates the minimum distance from a query point to a Minimum Bounding Rectangle (MBR). This function assesses the relationship of the
    query point with the boundaries of the MBR to determine the shortest possible distance. This calculation is fundamental in determining 
    the priority of node traversal in the best-first search algorithm by assessing potential proximity of nodes to the query point. For 
    efficiently finding the shortest distance three cases are considered separately:
    conditions
    -----------
    condition 1: MBR(x1) <= point(x) <= MBR(x2)
    condition 2: MBR(y1) <= point(y) <= MBR(y2) 

    cases
    ------
    case 1: if both consition 1 and 2are true it means that the point falls inside the MBR. Hence while calculating distance from point 
    to a side of MBR, these points will be ignored and assinged a distance of 0.
    case 2: if only one of the conditions are correct, that means this point is outside the MBR but a straight line with a right angle can 
    drawn from point to any of the 4 sides of MBR. Hence, if condition 1 is true, then shortest distance is just the distance between 
    point(x) and MBR(x1 or x2) where x1 or x2 will be determined based on the nearest side of the MBR. Same process for y, if condition 2 
    is only
    case 3: Both the condition being false means that the point is obviously outside of the MBR and no straight line with a right angle can
    be drawn from the point to any side of the MBR. As a result shortest distance is point to any of the corner.

    Args:
    mbr_coord (dict): A dictionary containing the coordinates of the MBR ('x1', 'y1' for the lower left and 'x2', 'y2' for the upper right corners).
    query (dict): A dictionary representing the query point with 'x' and 'y' coordinates.

    Returns:
    float: The calculated minimum distance from the query point to the MBR. This distance is zero if the query point is inside the MBR, calculated via direct geometry if on an edge, or derived from Pythagorean theorem if the query point is outside the nearest edges.
    """

    # Calculate minimum distance from a query point to a Minimum Bounding Rectangle (MBR)
    # Check if query point lies inside the MBR on both x and y axes
    inside_x = mbr_coord['x1'] <= query['x'] <= mbr_coord['x2']
    inside_y = mbr_coord['y1'] <= query['y'] <= mbr_coord['y2']

    if inside_x and inside_y:
        # If query point is inside the MBR, distance is zero
        distance = 0
    elif not inside_x and not inside_y:
        # Calculate nearest distance from point to MBR if outside on both axes
        x_distance = min(abs(query['x'] - mbr_coord['x1']), abs(query['x'] - mbr_coord['x2']))
        y_distance = min(abs(query['y'] - mbr_coord['y1']), abs(query['y'] - mbr_coord['y2']))
        distance = math.sqrt((x_distance**2 + y_distance**2))
    else:
        # Calculate distance if the point is outside MBR only on one axis
        if inside_x:
            distance = min(abs(query['y'] - mbr_coord['y1']), abs(query['y'] - mbr_coord['y2']))
        else:
            distance = min(abs(query['x'] - mbr_coord['x1']), abs(query['x'] - mbr_coord['x2']))
    
    return distance

def euclidean_distance(point1, point2):
    # Calculate Euclidean distance between two points in 2D space
    """
    Calculate the Euclidean distance between coordinates of parking and coordinates of query in 2D space.
    
    Args:
    point1 (list): A list of coordinates (x1, y1) for the first point (either parking or query).
    point2 (list): A list of coordinates (x2, y2) for the second point (either parking or query).

    Returns:
    float: The Euclidean distance between the parking point and query point.
    """

    distance = math.sqrt((point2['x'] - point1['x'])**2 + (point2['y'] - point1['y'])**2)
    return distance


def tree_traversal(bfs, rtree_root):
    """
    Recursively navigates through the R-tree to efficiently find the nearest point to the query. This function is integral to the Best-First
    Search (BFS) algorithm, strategically exploring nodes based on proximity to minimize search depth and computational cost. The function 
    prioritizes closest nodes as they have higher potential to contain the nearest point.

    Node Evaluation Cases:
    ----------------------
    case 1: Leaf Node Check
        - If the current node is a leaf, the function computes the Euclidean distance from the query point to each point in the leaf. The 
        point with the shortest distance is considered for updating the global minimum distance (mindist_point).
        - Early termination occurs if the closest point in the current leaf node is closer than any previously considered nodes, ensuring 
        efficiency. The reasoning behind this action is that, if a point is closer to query point than shortest distance to other MBRs, then
        it will definitely be closer to query point than any other point inside those MBRs.

    case 2: Internal Node Check
        - For internal nodes, the function calculates the minimum distance from the query point to each child's Minimum Bounding Rectangle 
        (MBR). It then sorts these children by distance, allowing the BFS algorithm to explore the closest nodes first.
        - This sorting and subsequent recursive traversal continue until a leaf node is encountered or all paths have been exhausted.

    Early Termination:
    ------------------
    - The function may terminate early if it is certain that no closer points can be found in the remaining nodes, based on the distances 
    stored in `mindist_mbrs`.

    Args:
    bfs (BFS instance): An instance of the BFS class managing the state of the search, including the list of nodes to explore and the minimum 
    distance found.
    rtree_root (R-tree node): The current node in the R-tree being evaluated, either a leaf or an internal node.

    Returns:
    bool: True if a closer point is found and the search can potentially be pruned; False otherwise. This boolean helps control the recursive 
    exploration of the tree.
    
    Detailed Execution Flow:
    ------------------------
    1. The function first checks if the current node (`rtree_root`) is in the list of nodes to explore (`bfs.mindist_mbrs`). If found, it's 
    removed to avoid redundant calculations.
    2. If `rtree_root` is a leaf, the distances to all data points within are calculated. The closest data point updates `bfs.mindist_point` 
    if it's closer than what was previously found.
    3. For internal nodes, the function calculates distances to child nodes' MBRs, sorts them, and recursively explores each child, starting
    with the closest. This step is repeated until no closer points are possible.
    4. A return value of True signals that the traversal has updated the minimum distance and may impact further exploration paths; False 
    indicates no update, suggesting further exploration may be needed.
    """
    # Recursive function to perform best first search
    # Remove the current node from the list if it matches the root node
    for item in bfs.mindist_mbrs:
        if rtree_root in item:
            bfs.mindist_mbrs.remove(item)
            break

    if not rtree_root.is_leaf():
        # If the node is not a leaf, calculate distance to each child's MBR and recurse
        for child_node in rtree_root.child_nodes:
            shortest_distance = mindist_point_to_MBR(child_node.MBR, bfs.query)
            bfs.mindist_mbrs.append([shortest_distance, child_node])

        bfs.mindist_mbrs.sort(key=lambda x: x[0])  # Sort the list by distance
        for item in bfs.mindist_mbrs:
            result = tree_traversal(bfs, item[1])
            if result:
                return True                    
        return False

    else:
        # Process leaf nodes by comparing distances of data points to the query point
        mindist_data_point = []
        for data_point in rtree_root.data_points:
            distance = euclidean_distance(data_point, bfs.query)
            mindist_data_point.append([distance, data_point])
        closest_data_point = min(mindist_data_point, key=lambda x: x[0])

        # Update the closest data point found so far if the current one is closer
        if bfs.mindist_point is None or closest_data_point[0] <= bfs.mindist_point[0]:
            bfs.mindist_point = closest_data_point

        # Early termination if no MBRs are closer than the closest data point found
        for item in bfs.mindist_mbrs:
            if item[0] < closest_data_point[0]:
                return False
        return True
    
if __name__ == '__main__':
    # Execute the main function if this script is run as the main program
    main()