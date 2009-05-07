function getElementsByClass(searchClass,node,tag) {

        var classElements = new Array();
        if (node == null)
                node = document;
        if (tag == null)
                tag = '*';
        var els = node.getElementsByTagName(tag);
        var elsLen = els.length;
        var pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)");
        var j = 0;
        for (i = 0; i < elsLen; i++) {
                if (pattern.test(els[i].className) ) {
                        classElements[j] = els[i];
                        j++;
                }
        }
        return classElements;
}
