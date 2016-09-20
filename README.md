Script that generates a Github contribution report for all repos belonging to
an organization.

# Instructions

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Generate a Github O-Auth token and modify the `OAUTH_TOKEN` assignment line
   in stats.py.
3. Set the `ORG` setting in stats.py to your org's Github name.
4. Run the script:
   ```
  ./stats.py
  ```


Example output:

```
========================Stats for fake_org/fake_repo==========================

       thomasw:       5 commits      1250 ++        32 --
       foouser:      10 commits       100 ++        14 --

======================Stats for fake_org/fake_repo1===========================

       baruser:       1 commits         2 ++         1 --
       thomasw:       1 commits         2 ++         2 --

================================Leader Boards=================================

Number of commits:

  1.         foouser:      10 commits       100 ++        14 --     1 repos
                                                              since 2012-02-25

  2.         thomasw:       6 commits      1252 ++        34 --    2 repos
                                                              since 2012-03-10

  3.         baruser:       1 commits         2 ++         2 --     1 repos
                                                              since 2006-06-24

Lines of code added:

  1.         thomasw:       6 commits      1252 ++        34 --    2 repos
                                                              since 2012-03-10

  2.         foouser:      10 commits       100 ++        14 --     1 repos
                                                              since 2012-02-25

  3.         baruser:       1 commits         2 ++         2 --     1 repos
                                                              since 2006-06-24

Lines of code deleted:

  1.         thomasw:       6 commits      1252 ++        34 --    2 repos
                                                              since 2012-03-10

  2.         foouser:      10 commits       100 ++        14 --     1 repos
                                                              since 2012-02-25

  3.         baruser:       1 commits         2 ++         2 --     1 repos
                                                              since 2006-06-24



* Note: This only includes stats from master branches.

* Note: Contributors are not limited to fake_org members.

```
