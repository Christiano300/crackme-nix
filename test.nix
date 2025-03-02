let
                baem0Ame = (builtins.tail (builtins.tail [1 2 3 4]));
              in
              [
                (builtins.head (builtins.tail [1 2 3 4]))
                (builtins.head [1 2 3 4])
              ]
              ++ baem0Ame
