import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Link from '@tiptap/extension-link';
import { ActionIcon, Group, Paper } from '@mantine/core';
import {
  IconBold, IconItalic, IconStrikethrough, IconList, IconListNumbers, IconLink, IconUnlink,
} from '@tabler/icons-react';

interface WYSIWYGEditorProps {
  value: string;
  onChange: (value: string) => void;
}

export function WYSIWYGEditor({ value, onChange }: WYSIWYGEditorProps) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Link.configure({ openOnClick: false }),
    ],
    content: value,
    onUpdate: ({ editor }) => onChange(editor.getHTML()),
  });

  if (!editor) return null;

  const setLink = () => {
    const url = window.prompt('URL', editor.getAttributes('link').href);
    if (url === null) return;
    if (url === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();
    } else {
      editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run();
    }
  };

  return (
    <Paper withBorder p={0}>
      <Group gap={4} p="xs" style={{ borderBottom: '1px solid var(--mantine-color-default-border)' }}>
        <ActionIcon
          variant={editor.isActive('bold') ? 'filled' : 'subtle'}
          size="sm"
          onClick={() => editor.chain().focus().toggleBold().run()}
          aria-label="Bold"
        >
          <IconBold size={14} />
        </ActionIcon>
        <ActionIcon
          variant={editor.isActive('italic') ? 'filled' : 'subtle'}
          size="sm"
          onClick={() => editor.chain().focus().toggleItalic().run()}
          aria-label="Italic"
        >
          <IconItalic size={14} />
        </ActionIcon>
        <ActionIcon
          variant={editor.isActive('strike') ? 'filled' : 'subtle'}
          size="sm"
          onClick={() => editor.chain().focus().toggleStrike().run()}
          aria-label="Strikethrough"
        >
          <IconStrikethrough size={14} />
        </ActionIcon>
        <ActionIcon
          variant={editor.isActive('bulletList') ? 'filled' : 'subtle'}
          size="sm"
          onClick={() => editor.chain().focus().toggleBulletList().run()}
          aria-label="Bullet list"
        >
          <IconList size={14} />
        </ActionIcon>
        <ActionIcon
          variant={editor.isActive('orderedList') ? 'filled' : 'subtle'}
          size="sm"
          onClick={() => editor.chain().focus().toggleOrderedList().run()}
          aria-label="Ordered list"
        >
          <IconListNumbers size={14} />
        </ActionIcon>
        <ActionIcon
          variant={editor.isActive('link') ? 'filled' : 'subtle'}
          size="sm"
          onClick={setLink}
          aria-label="Add link"
        >
          <IconLink size={14} />
        </ActionIcon>
        <ActionIcon
          variant="subtle"
          size="sm"
          onClick={() => editor.chain().focus().unsetLink().run()}
          disabled={!editor.isActive('link')}
          aria-label="Remove link"
        >
          <IconUnlink size={14} />
        </ActionIcon>
      </Group>
      <EditorContent editor={editor} style={{ padding: '8px 12px', minHeight: 120 }} />
    </Paper>
  );
}
