import os
import sys
import javalang
import xml.etree.ElementTree as ET

# アクセス修飾子のマッピング
def get_modifier(modifiers):
    if not modifiers:
        return '~'  # パッケージプライベート（デフォルト）
    if 'private' in modifiers:
        return '-'
    if 'protected' in modifiers:
        return '#'
    if 'public' in modifiers:
        return '+'
    return '~'

# クラスやインターフェースをパース
def parse_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    tree = javalang.parse.parse(code)
    return tree

# クラス情報をUMlet形式の文字列に変換
def class_to_panel_attributes(class_node):
    name = class_node.name
    is_interface = isinstance(class_node, javalang.tree.InterfaceDeclaration)
    is_abstract = 'abstract' in (class_node.modifiers or [])

    header = name
    if is_interface:
        header = f"<<interface>>\n{name}"
    elif is_abstract:
        header = f"&lt;&lt;abstract&gt;&gt;\\n{name}"

    fields = []
    constructors = []
    methods = []

    # フィールド情報
    for field in getattr(class_node, 'fields', []):
        for decl in field.declarators:
            modifier = get_modifier(field.modifiers)
            type_str = str(field.type.name if hasattr(field.type, 'name') else field.type)
            fields.append(f"{modifier}{decl.name}: {type_str}")

    # コンストラクタ情報
    for constructor in getattr(class_node, 'constructors', []):
        modifier = get_modifier(constructor.modifiers)
        params = ', '.join(f"{p.name}: {p.type.name}" for p in constructor.parameters)
        methods.append(f"{modifier}{constructor.name}({params})")

    # メソッド情報
    for method in getattr(class_node, 'methods', []):
        modifier = get_modifier(method.modifiers)
        ret_type = str(method.return_type.name if method.return_type else 'void')
        params = ', '.join(f"{p.name}: {p.type.name}" for p in method.parameters)
        methods.append(f"{modifier}{method.name}({params}): {ret_type}")

    field_section = '\n'.join(fields)
    constructor_section = '\n'.join(constructors)
    method_section = '\n'.join(methods)

    return f"{header}\n--\n{field_section}\n--\n{constructor_section}\n--\n{method_section}"

# クラスをUMlet用XMLのelementに変換
def create_uml_element(panel_attributes, x=20, y=20):
    element = ET.Element("element")
    ET.SubElement(element, "id").text = "UMLClass"
    coords = ET.SubElement(element, "coordinates")
    ET.SubElement(coords, "x").text = str(x)
    ET.SubElement(coords, "y").text = str(y)
    ET.SubElement(coords, "w").text = "120"
    ET.SubElement(coords, "h").text = "150"
    ET.SubElement(element, "panel_attributes").text = panel_attributes
    ET.SubElement(element, "additional_attributes")
    return element

# ディレクトリ or 単一ファイルの処理
def collect_classes_from_path(input_path):
    java_files = []
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
    elif os.path.isfile(input_path) and input_path.endswith(".java"):
        java_files = [input_path]
    return java_files

# メイン処理
def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py output.uxf input.java|input_dir/")
        sys.exit(1)

    output_file = sys.argv[1]
    input_path = sys.argv[2]

    diagram = ET.Element("diagram")
    java_files = collect_classes_from_path(input_path)

    x_offset = 20
    for file in java_files:
        try:
            tree = parse_java_file(file)
            for type_decl in tree.types:
                panel_text = class_to_panel_attributes(type_decl)
                element = create_uml_element(panel_text, x=x_offset, y=20)
                diagram.append(element)
                x_offset += 200
        except Exception as e:
            print(f"Error processing {file}: {e}")

    tree = ET.ElementTree(diagram)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"UMlet diagram saved to: {output_file}")

if __name__ == "__main__":
    main()
