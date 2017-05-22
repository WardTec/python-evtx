from fixtures import *

import Evtx.Evtx as evtx
import Evtx.Nodes as e_nodes


def test_parse_records(system):
    '''
    regression test demonstrating that all record metadata can be parsed.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    '''
    fh = evtx.FileHeader(system, 0x0)
    for i, chunk in enumerate(fh.chunks()):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2a2a


def test_parse_records2(security):
    '''
    regression test demonstrating that all record metadata can be parsed.

    Args:
      security (bytes): the security.evtx test file contents. pytest fixture.
    '''
    fh = evtx.FileHeader(security, 0x0)
    for i, chunk in enumerate(fh.chunks()):
        for j, record in enumerate(chunk.records()):
            assert record.magic() == 0x2a2a


def one(iterable):
    '''
    fetch a single element from the given iterable.

    Args:
      iterable (iterable): a sequence of things.

    Returns:
      object: the first thing in the sequence.
    '''
    for i in iterable:
        return i


def extract_structure(node):
    '''
    given an evtx bxml node, generate a tree of all the nodes.
    each node has:
      - str: node type
      - str: (optional) value
      - list: (optional) children

    Args:
      node (evtx.Node): the root node.

    Returns:
      list: the tree representing the bxml structure.
    '''
    name = node.__class__.__name__

    if isinstance(node, e_nodes.BXmlTypeNode):
        # must go before is VariantTypeNode
        value = None
    elif isinstance(node, e_nodes.VariantTypeNode):
        value = node.string()
    elif isinstance(node, e_nodes.OpenStartElementNode):
        value = node.tag_name()
    elif isinstance(node, e_nodes.AttributeNode):
        value = node.attribute_name().string()
    else:
        value = None

    children = []
    if isinstance(node, e_nodes.BXmlTypeNode):
        children.append(extract_structure(node._root))
    elif isinstance(node, e_nodes.TemplateInstanceNode) and node.is_resident_template():
        children.append(extract_structure(node.template()))

    children.extend(list(map(extract_structure, node.children())))

    if isinstance(node, e_nodes.RootNode):
        substitutions = list(map(extract_structure, node.substitutions()))
        children.append(['Substitutions', None, substitutions])

    if children:
        return [name, value, children]
    elif value:
        return [name, value]
    else:
        return [name]


def test_parse_record(system):
    '''
    regression test demonstrating binary xml nodes getting parsed.

    Args:
      system (bytes): the system.evtx test file contents. pytest fixture.
    '''
    fh = evtx.FileHeader(system, 0x0)
    chunk = one(fh.chunks())
    record = one(chunk.records())

    # generated by hand, but matches the output of extract_structure.
    expected = \
      ['RootNode', None, [
        ['StreamStartNode'],
        ['TemplateInstanceNode', None, [
          ['TemplateNode', None, [
            ['StreamStartNode'],
            ['OpenStartElementNode', 'Event', [
              ['AttributeNode', 'xmlns', [
                ['ValueNode', None, [
                  ['WstringTypeNode', 'http://schemas.microsoft.com/win/2004/08/events/event']]]]],
              ['CloseStartElementNode'],
              ['OpenStartElementNode', 'System', [
                ['CloseStartElementNode'],
                ['OpenStartElementNode', 'Provider', [
                  ['AttributeNode', 'Name', [
                    ['ValueNode', None, [
                      ['WstringTypeNode', 'Microsoft-Windows-Eventlog']]]]],
                  ['AttributeNode', 'Guid', [
                    ['ValueNode', None, [
                      ['WstringTypeNode', '{fc65ddd8-d6ef-4962-83d5-6e5cfe9ce148}']]]]],
                  ['CloseEmptyElementNode']]],
                ['OpenStartElementNode', 'EventID', [
                  ['AttributeNode', 'Qualifiers', [
                    ['ConditionalSubstitutionNode']]],
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Version', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Level', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Task', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Opcode', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Keywords', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'TimeCreated', [
                  ['AttributeNode', 'SystemTime', [
                    ['ConditionalSubstitutionNode']]],
                  ['CloseEmptyElementNode']]],
                ['OpenStartElementNode', 'EventRecordID', [
                  ['CloseStartElementNode'],
                  ['ConditionalSubstitutionNode'],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Correlation', [
                  ['AttributeNode', 'ActivityID', [
                    ['ConditionalSubstitutionNode']]],
                  ['AttributeNode', 'RelatedActivityID', [
                    ['ConditionalSubstitutionNode']]],
                  ['CloseEmptyElementNode']]],
                ['OpenStartElementNode', 'Execution', [
                  ['AttributeNode', 'ProcessID', [
                    ['ConditionalSubstitutionNode']]],
                  ['AttributeNode', 'ThreadID', [
                    ['ConditionalSubstitutionNode']]],
                  ['CloseEmptyElementNode']]],
                ['OpenStartElementNode', 'Channel', [
                  ['CloseStartElementNode'],
                  ['ValueNode', None, [
                    ['WstringTypeNode', 'System']]],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Computer', [
                  ['CloseStartElementNode'],
                  ['ValueNode', None, [
                    ['WstringTypeNode', 'WKS-WIN764BITB.shieldbase.local']]],
                  ['CloseElementNode']]],
                ['OpenStartElementNode', 'Security', [
                  ['AttributeNode', 'UserID', [
                    ['ConditionalSubstitutionNode']]],
                  ['CloseEmptyElementNode']]],
                ['CloseElementNode']]],
              ['OpenStartElementNode', 'UserData', [
                ['CloseStartElementNode'],
                ['ConditionalSubstitutionNode'],
                ['CloseElementNode']]],
              ['CloseElementNode']]],
            ['EndOfStreamNode']]]]],
        ['Substitutions', None, [
          ['UnsignedByteTypeNode', '4'],
          ['UnsignedByteTypeNode', '0'],
          ['UnsignedWordTypeNode', '105'],
          ['UnsignedWordTypeNode', '105'],
          ['NullTypeNode'],
          ['Hex64TypeNode', '0x80000000000000'],
          ['FiletimeTypeNode', '2012-03-14T04:17:43.354563Z'],
          ['NullTypeNode'],
          ['UnsignedDwordTypeNode', '820'],
          ['UnsignedDwordTypeNode', '2868'],
          ['UnsignedQwordTypeNode', '12049'],
          ['UnsignedByteTypeNode', '0'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['NullTypeNode'],
          ['BXmlTypeNode', None, [
            ['RootNode', None, [
              ['StreamStartNode'],
              ['TemplateInstanceNode', None, [
                  ['TemplateNode', None, [
                    ['StreamStartNode'],
                    ['OpenStartElementNode', 'AutoBackup', [
                      ['AttributeNode', 'xmlns:auto-ns3', [
                        ['ValueNode', None, [
                          ['WstringTypeNode', 'http://schemas.microsoft.com/win/2004/08/events']]]]],
                      ['AttributeNode', 'xmlns', [
                        ['ValueNode', None, [
                          ['WstringTypeNode', 'http://manifests.microsoft.com/win/2004/08/windows/eventlog']]]]],
                      ['CloseStartElementNode'],
                      ['OpenStartElementNode', 'Channel', [
                        ['CloseStartElementNode'],
                        ['NormalSubstitutionNode'],
                        ['CloseElementNode']]],
                      ['OpenStartElementNode', 'BackupPath', [
                        ['CloseStartElementNode'],
                        ['NormalSubstitutionNode'],
                        ['CloseElementNode']]],
                      ['CloseElementNode']]],
                    ['EndOfStreamNode']]]]],
              ['Substitutions', None, [
                ['WstringTypeNode', 'System'],
                ['WstringTypeNode', 'C:\Windows\System32\Winevt\Logs\Archive-System-2012-03-14-04-17-39-932.evtx']]]]]]]]]]]

    assert extract_structure(record.root()) == expected
