# Changelog

## 0.4 (2023-08-12)

* Merge [#12: Fix TypeError during run](https://github.com/brightway-lca/bw_recipe_2016/pull/12). Thanks @ChristinaKockel!
* Merge [#9: Fix bug: IndexError: tuple index out of range](https://github.com/brightway-lca/bw_recipe_2016/pull/9). Thanks @BenPortner!
* Merge [#7: Bug fixes for importing ReCiPe 2016 impact categories into bw projects](https://github.com/brightway-lca/bw_recipe_2016/pull/7). Thanks @juweya!
* Merge [#5: Documentation fixes](https://github.com/brightway-lca/bw_recipe_2016/pull/5). Thanks @lvandepaer!
* Fix [#13: Remove psutil dependency](https://github.com/brightway-lca/bw_recipe_2016/issues/13)

## 0.3 (2020-06-09)

* Support three different versions of ReCiPe
* Fix duplicate characterization factors by solving various problems in ecoinvent and the ReCiPe data
* Fix some matching bugs that caused duplicate CFs

#### 0.2.1 (2020-05-22)

* Added a weighted single score indicator

## 0.2 (2020-05-22)

* `add_recipe_2016` not deletes ReCiPe before importing it
* Fix error with `match_cas_numbers` not following the given categories and subcategories
* Deleted duplicate air category in toxicity matching
* Fixed sign for water CFs

### 0.1.1 (2020-05-20)

* Added more water categories to eutrophication
* Created aggregated ecosystems total endpoint methods
* Change handling of `iron` and `iron ore` in mineral resources

## 0.1 (2020-05-20)

Initial release
