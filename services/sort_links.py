def sort_links_by_matching(links, keywords):

    links = list(dict.fromkeys(links)) #remove doubles by transforming into dict
    only_topic = []
    for i in range(0, len(links)):
        only_topic.append(links[i][0])

    listA = list(only_topic)

    list_with_matching_coefficients = []
    new_links_list = []
    for m in range(0, len(listA)):
        current = []
        element = listA[m]
        #print("current element: " + str(element))
        current.append(element)
        current_list_a = " ".join(current).split()
        #print("current_list_a: " + str(current_list_a))
        #print("listB: " + str(keywords))
        setA = set(current_list_a)
        setB = set(keywords)

        overlap = setA & setB

        matching = float(len(overlap)) / len(setB) * 100
        if matching > 0:

            #print("current coefficient: " + str(matching))
            list_with_matching_coefficients.append(matching)
            new_links_list.append(links[m])
    #print("list with matching coefficients: " + str(list_with_matching_coefficients))
    #print("new links list: " + str(new_links_list))
    #sort list based on list with matching coefficients

    sorted_list = [x for _,x in sorted(zip(list_with_matching_coefficients, new_links_list))]
    sorted_list.reverse()
    #print("sorted_list: " + str(sorted_list))

    #each list element contains topic + link
    all_links = []
    if len(sorted_list) > 0:
        for j in range(0, len(sorted_list)):
            #print("current element: " + str(sorted_list[j][1]))
            all_links.append(sorted_list[j][1])   #only return link, not whole tuple
    #print("all links: " + str(all_links))
    all_links = list(dict.fromkeys(all_links)) #potentially two topics have same link; remove from list
    return all_links
