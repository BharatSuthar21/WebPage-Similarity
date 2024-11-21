import requests
import sys



# Function for fetching Body's content only text from url's content
def body_fetch(content):
    start_index = content.find('<body')
    end_index = content.find('/body>')+6
    content = content[start_index:end_index]
    
    while '<script' in content:
        start_index = content.find('<script')
        end_index = content.find('/script>')+8
        content = (content[:start_index] + content[end_index:])
    while '<style' in content:
        start_index = content.find('<style')
        end_index = content.find('/style>')+7
        content = (content[:start_index] + content[end_index:])
        

    data = []

    while '<' in content:
        start_index = content.find('<')
        end_index = content.find('>')+1

        if content[start_index: start_index+2] == '<p':
            ps = content.find('<p')
            pe = content.find('/p>')+3
            sub_content = content[ps:pe]
            content = content[pe:]
            data.append(body_helper(sub_content))
        elif content[start_index: start_index+3] == '<li':
            lis = content.find('<li')
            lie = content.find('/li>')+4
            sub_content = content[lis:lie]
            content = content[lie:]
            data.append(body_helper(sub_content))
        else:
            result = content[:start_index].strip()
            content = content[end_index:]
            if len(result) >1:
                data.append(result)
    return data


def body_helper(content):

    result = ""
    while '<' in content:
        s_ind = content.find('<')
        e_ind = content.find('>')+1
        if len(content[:s_ind].strip()) > 1:
            result += content[:s_ind].strip()+" "
        content = content[e_ind:]
    return result.strip()



def PrintBodyContent(content):
    content = body_fetch(content)
    result = []
    for i in content:
        while '&#' in i:
            s = i.find('&#')
            e = i.find(';', s)
            i = i[:s] + " "+i[e]
        if i[0:2] in [' ,', ' .', ' ;', " '", ";", ". ", ", ", ": "]:
            i = i[2:]
        if len(i) > 1 or i.isalnum():
            result.append(i)
    return result






def ngram(content, n):
    """
    Return a list containg ngrams of the document
    
    """

    cont = []
    for i in content:
        cont+=i.split()
        
    ngrams = []
    for i in range(len(cont)-1-n):
        sub_string = ""
        for j in cont[i:i+n]:
            sub_string+=j+" "
        ngrams.append(sub_string.strip())
    return ngrams





def frequency(doc):
    """
    Return the frequency of words or ngrams of the document
    """
    dict = {}

    for i in doc:
        if i in dict:
            dict[i]+=1
        else:
            dict[i]=1
    return dict





def simHash(doc, p=53, m=2**64):
    """
    return the simhash of each ngram or word of the document
    """
    hash_dic = {}
    
    for i in doc:
        score = 0
        count = 0
        for j in i:
            score += ord(j)*(p**count)
            count+=1
        
        hash_dic[i] = decimal_to_binary(score%m)
    return hash_dic
    

def decimal_to_binary(num):
    binary_rep = str(bin(num))[2:]
    return "0"*(64 - len(binary_rep))+binary_rep





def simVector(doc, freq):
    """
    return the vector of the simhash
    """
    vector = [0]*64
    for i in doc:
        for j in range(64):
            value = doc[i]
            if value[j] == '1':
                vector[j] += 1* freq[i]
            else:
                vector[j] -= 1*freq[i] 
    return vector





def fingerPrint(doc):
    """
    Return the fingerprint of the document
    """
    result = ""
    for i in doc:
        if i < 0:
            result+='0'
        else:
            result+='1'
    return result





def bit_similirity(doc1, doc2):
    count = 0
    for i, j in zip(doc1, doc2):
        if i == j:
            count+=1
    return str(count *100 / 64)+"%"






if __name__ == '__main__':
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    n = int(sys.argv[3])

    

    try:

        # for url1
        response = requests.get(url1)
        response = response.text.lower()
        hash1 = fingerPrint(simVector(simHash(frequency(ngram(PrintBodyContent(response),n))), frequency(ngram(PrintBodyContent(response),n))))
        print("Fingerprint for url {} is ".format(url1)+hash1)

        
        # for url2
        response = requests.get(url2)
        response = response.text.lower()
        hash2 = fingerPrint(simVector(simHash(frequency(ngram(PrintBodyContent(response),n))), frequency(ngram(PrintBodyContent(response),n))))
        print("Fingerprint for url {} is ".format(url1)+hash2)


        print(bit_similirity(hash1, hash2))


    except:
        print("Enable to find response. Facing some problem")