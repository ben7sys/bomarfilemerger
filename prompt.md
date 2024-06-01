Improve the python script.
Add the missing Elements.

Folders:
Foldernames (<H>)

Links:
DATA-IMPORTANT
DATA-COVER
TAGS
ICON_URI
LAST_CHARSET




---


# Task
Create a python script code base. 
Convert a bookmark file into a structured json file.
Ignore Folders, only convert links.
The source and destination should be a variable.

## HTML Structure:
Folders:
    <H3>
        ADD_DATE
        LAST_MODIFIED
    </H3>

Link Description:
    <A>
        HREF
        ADD_DATE
        LAST_MODIFIED
        ICON
        
    </A>
 
## Example bookmark_example.html
```html
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1714341278" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">Toolbar Folder</H3>
    <DL><p>
    </DL><p>
    <DT><A HREF="https://some.link" ADD_DATE="1717122539" ICON="data:image/png;base64,iVBORw0AElFTkSuQmCC">Link Description</A>
    <DT><H3 ADD_DATE="1714683750" LAST_MODIFIED="1714821517">Folder 1</H3>
    <DL><p>
        <DT><A HREF="https://some.link" ADD_DATE="1714683750" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAASUVORK5CYII=">Link Description</A>
    </DL><p>
    <DT><A HREF="https://something.com" ADD_DATE="1665802514" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA6oOCD0rfZHzAAAAAElFTkSuQmCC">Link Description</A>
    <DT><A HREF="https://any.example" ADD_DATE="1714821517" ICON="data:image/png;base64,iVBORmG4DeQn7o9XwoccgAAAABJRU5ErkJggg==">Link Description</A>
    <DT><H3 ADD_DATE="1715043097" LAST_MODIFIED="1715043097">Folder 2</H3>
    <DL><p>
        <DT><H3 ADD_DATE="1715043097" LAST_MODIFIED="1715043097">Subfolder 1</H3>
        <DL><p>
            <DT><A HREF="https://any.example" ADD_DATE="1715043097" ICON="data:image/png;base64,iVBORw0KGgoAv/dmPAbv2kmCC">Link Description</A>
            <DT><A HREF="https://some.link" ADD_DATE="1715043097" ICON="data:image/png;base64,iVBORw0KGAAAAElFTkSuQmCC">Link Description</A>
        </DL><p>
    </DL><p>
</DL><p>
```

# JSON Structure EXAMPLE:
```json
{
    "bookmarks": [
        {
            "url": "https://some.link",
            "description": "Link Description",
            "icon": "data:image/png;base64,iVBORw0AElFTkSuQmCC",
            "add_date": "1717122539",
            "last_modified": "0"
        },
        {
            "url": "https://some.link",
            "description": "Link Description",
            "icon": "data:image/png;base64,iVBORw0KGAAAAElFTkSuQmCC",
            "add_date": "1715043097",
            "last_modified": "1715043097"
        }
    ]
}
```

