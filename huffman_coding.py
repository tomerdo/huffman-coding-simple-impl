from typing import Dict
import queue


class HuffmanNode:
    terminal = False
    left = right = None
    amount = -1
    letter = None

    def __init__(self, letter, amount, terminal=True, left=None, right=None):
        self.letter = letter
        self.amount = amount
        self.terminal = terminal
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.amount < other.amount


def compute_frequency(txt: str) -> Dict:
    res = {}
    for c in txt:
        if c in res:
            res[c] += 1
        else:
            res[c] = 1
    return res


def create_huffman_tree(txt: str) -> HuffmanNode:
    p_queue = queue.PriorityQueue()
    freq_dict = compute_frequency(txt)
    for c, amount in freq_dict.items():
        node = HuffmanNode(c, amount)
        p_queue.put(node)

    while p_queue.qsize() > 1:
        first = p_queue.get()
        second = p_queue.get()
        parent_node = HuffmanNode(first.letter + second.letter, first.amount + second.amount, False, second, first)
        p_queue.put(parent_node)

    # root
    return p_queue.get()


def encode_txt(txt: str) -> (str, Dict):
    root = create_huffman_tree(txt)
    coding_dict = from_tree_to_dict(root)
    encoded_txt = ''
    for c in txt:
        encoded_txt += coding_dict[c]
    return encoded_txt, coding_dict


def from_tree_to_dict(root: HuffmanNode) -> Dict:
    res = {}
    queue_traversal = [(root, '')]
    while len(queue_traversal) > 0:
        element, path = queue_traversal.pop(0)
        if element.terminal:
            res[element.letter] = path
        else:
            if element.right:
                queue_traversal.append((element.right, path + '1'))
            if element.left:
                queue_traversal.append((element.left, path + '0'))
    return res


def decode_txt(encrypted_txt: str, huffman_dict: Dict) -> str:
    reverse_dict = {v: k for k, v in huffman_dict.items()}
    current_code = ''
    decoded_txt = ''
    for c in encrypted_txt:
        current_code += c
        if current_code in reverse_dict:
            decoded_txt += reverse_dict[current_code]
            current_code = ''
    return decoded_txt


def main():
    txt = input('Please enter your text')
    print(f'the text we want to encode {txt}')

    encoded_txt, coding_dict = encode_txt(txt)
    print(f'After encoding huffman {encoded_txt}, {coding_dict}')

    print('decoded text', decode_txt(encoded_txt, coding_dict))

    print(
        f'compressed size: {len(encoded_txt)}, original size: {len(txt) * 8} compressing ration {len(encoded_txt) / (len(txt) * 8)}')


if __name__ == '__main__':
    main()
