let aHi5cahr =
    string:
    builtins.genList (index: builtins.substring index 1 string) (
      builtins.stringLength string
    );
    in
    aHi5cahr "hallo"
