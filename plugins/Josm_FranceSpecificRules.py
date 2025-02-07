#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re # noqa

from plugins.Plugin import with_options # noqa
from plugins.PluginMapCSS import PluginMapCSS


class Josm_FranceSpecificRules(PluginMapCSS):

    MAPCSS_URL = 'https://josm.openstreetmap.de/wiki/Rules/FranceSpecificRules'


    def init(self, logger):
        super().init(logger)
        tags = capture_tags = {} # noqa
        self.errors[20806] = self.def_class(item = 2080, level = 3, tags = mapcss.list_('parking', 'amenity', 'fix:chair'), title = mapcss.tr('Missing tag carpool on area'))
        self.errors[21600] = self.def_class(item = 2160, level = 3, tags = mapcss.list_('tag', 'railway'), title = mapcss.tr('Missing tag gauge on rail'))
        self.errors[30401] = self.def_class(item = 3040, level = 3, tags = mapcss.list_('ref', 'infrastructure', 'telecom'), title = mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}')))
        self.errors[30402] = self.def_class(item = 3040, level = 3, tags = mapcss.list_('ref', 'infrastructure', 'power'), title = mapcss.tr('missing tag'))
        self.errors[30403] = self.def_class(item = 3040, level = 3, tags = mapcss.list_('ref', 'infrastructure', 'telecom'), title = mapcss.tr('missing tag'))
        self.errors[40103] = self.def_class(item = 4010, level = 3, tags = mapcss.list_('tag', 'infrastructure', 'power'), title = mapcss.tr('deprecated tagging'))
        self.errors[40104] = self.def_class(item = 4010, level = 3, tags = mapcss.list_('ref', 'infrastructure', 'power'), title = mapcss.tr('deprecated tagging'))
        self.errors[40105] = self.def_class(item = 4010, level = 3, tags = [], title = mapcss.tr('misused tag in this country'))
        self.errors[40612] = self.def_class(item = 4061, level = 2, tags = mapcss.list_('parking', 'amenity', 'fix:chair'), title = mapcss.tr('Does this station still sell SP95, or has it been replaced by the SP95-E10?'))
        self.errors[9019001] = self.def_class(item = 9019, level = 3, tags = mapcss.list_('ref', 'highway'), title = mapcss.tr('validation rules highway milestone'))
        self.errors[9019002] = self.def_class(item = 9019, level = 3, tags = mapcss.list_('ref', 'highway'), title = mapcss.tr('validation rules nat_ref in France'))
        self.errors[9019003] = self.def_class(item = 9019, level = 3, tags = [], title = mapcss.tr('missing tag'))
        self.errors[9019004] = self.def_class(item = 9019, level = 3, tags = [], title = {'en': 'Unusual ref for motorway_junction; use of \'ref=*\' for the exit destination ref?'})

        self.re_045a0f34 = re.compile(r'(?i)co.?voiturage')
        self.re_0c53237c = re.compile(r'^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$')
        self.re_107d2c86 = re.compile(r'PT[1-9]{1}[0-9]*')
        self.re_173ac8d4 = re.compile(r'[0-9]{5}[A-Z0-9]{3}')
        self.re_23d0d993 = re.compile(r'[A-Z0-9]{3}')
        self.re_299ea34e = re.compile(r'^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$')
        self.re_30299d59 = re.compile(r'^(Enedis|GRDF)$')
        self.re_3863901a = re.compile(r'^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$')
        self.re_3b90619c = re.compile(r'^\D')
        self.re_4bae79a8 = re.compile(r'[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}')
        self.re_55ee32ac = re.compile(r'^(motorway|trunk|primary|secondary|tertiary)$')
        self.re_6388df2b = re.compile(r'^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$')
        self.re_6ac6c83c = re.compile(r'^(pole|tower)$')
        self.re_7510958f = re.compile(r'^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/(?i)co.?voiturage/][amenity][amenity!=car_pooling][!carpool][inside("FR")]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'car_pooling', 'car_pooling')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'carpool')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                # -osmoseAssertMatchWithContext:list("node name='Aire de Covoiturage' amenity=parking","inside=FR")
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr('Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','car_pooling'],
                    ['carpool','designated']])
                }})

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if ('amenity' in keys and 'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'fuel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, 'yes')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'fuel:e10')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr('Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if ('operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'operator') == mapcss._value_capture(capture_tags, 0, 'ERDF')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['operator','Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if ('ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:ERDF:gdo')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref:FR:gdo', mapcss.tag(tags, 'ref:ERDF:gdo')]]),
                    '-': ([
                    'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if ('ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:gdo')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, '[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if ('operator' in keys and 'power' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'substation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, 'operator'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'switch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 3, tags, 'operator') == mapcss._value_capture(capture_tags, 3, 'Enedis')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # node[power=~/^(pole|tower)$/][!operator][inside("FR")]
        if ('power' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6ac6c83c), mapcss._tag_capture(capture_tags, 0, tags, 'power'))) and (not mapcss._tag_capture(capture_tags, 1, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 9019003, 'subclass': 567532769, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if ('ref:FR:ARCEP' in keys) or ('ref:FR:Orange' in keys) or ('ref:FR:PTT' in keys) or ('ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom') != mapcss._value_const_capture(capture_tags, 1, 'connection_point', 'connection_point')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:SFR')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'copper', 'copper')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *["ref:FR:Orange"]["ref:FR:Orange"!~/PT[1-9]{1}[0-9]*/][inside("FR")]
        if ('ref:FR:Orange' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_107d2c86, 'PT[1-9]{1}[0-9]*'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like PT123 without trailing zeros","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like PT123 without trailing zeros', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:Orange:NRO"]["ref:FR:Orange:NRO"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:Orange:NRO' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange:NRO')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange:NRO'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT"]["ref:FR:PTT"!~/[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23d0d993, '[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT:NRA"]["ref:FR:PTT:NRA"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT:NRA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT:NRA')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT:NRA'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # node[highway=milestone][operator][nat_ref][nat_ref!~/^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$/][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'milestone')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator')) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_7510958f, '^(([1-9][0-9]|0[1-9])PR([0-9]|[1-9][0-9]|[1-9][0-9][0-9])[DGU](|C))$'), mapcss._tag_capture(capture_tags, 3, tags, 'nat_ref'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules highway milestone")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} is not a milestone valid reference RIU","{2.tag}")
                # -osmoseAssertNoMatchWithContext:list("node highway=milestone distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr('{0} is not a milestone valid reference RIU', mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # node[highway=milestone][operator][nat_ref][!distance][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'milestone')) and (mapcss._tag_capture(capture_tags, 1, tags, 'operator')) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'distance')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules highway milestone")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019001/3"
                # throwWarning:tr("missing distance")
                # -osmoseAssertNoMatchWithContext:list("node highway=milestone distance=38 nat_ref=77PR38DC operator=SANEF","inside=FR")
                # -osmoseAssertMatchWithContext:list("node highway=milestone nat_ref=77PR38DC operator=SANEF","inside=FR")
                err.append({'class': 9019001, 'subclass': 0, 'text': mapcss.tr('missing distance')})

        # node[highway=motorway_junction][ref=~/^\D/]
        if ('highway' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway') == mapcss._value_capture(capture_tags, 0, 'motorway_junction')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b90619c), mapcss._tag_capture(capture_tags, 1, tags, 'ref'))))
                except mapcss.RuleAbort: pass
            if match:
                # suggestAlternative:"'destination:ref=*' tag on the exiting 'highway=*_link'"
                # throwWarning:"Unusual ref for motorway_junction; use of 'ref=*' for the exit destination ref?"
                # fixRemove:"ref"
                # assertMatch:"node highway=motorway_junction ref=N7"
                err.append({'class': 9019004, 'subclass': 323412661, 'text': {'en': 'Unusual ref for motorway_junction; use of \'ref=*\' for the exit destination ref?'}, 'allow_fix_override': True, 'fix': {
                    '-': ([
                    'ref'])
                }})

        # *[amenity=kindergarten][school:FR=maternelle]
        if ('amenity' in keys and 'school:FR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'kindergarten')) and (mapcss._tag_capture(capture_tags, 1, tags, 'school:FR') == mapcss._value_capture(capture_tags, 1, 'maternelle')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misused tag in this country")
                # -osmoseItemClassLevel:"4010/40105/3"
                # throwWarning:"amenity=kindergarten is no longer used for an 'école maternelle' in France, use amenity=school"
                # suggestAlternative:"amenity=school"
                # fixAdd:"amenity=school"
                err.append({'class': 40105, 'subclass': 0, 'text': {'en': 'amenity=kindergarten is no longer used for an \'école maternelle\' in France, use amenity=school'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','school']])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[railway=rail][!gauge][inside("FR")]
        if ('railway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'railway') == mapcss._value_capture(capture_tags, 0, 'rail')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'gauge')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("tag","railway")
                # -osmoseItemClassLevel:"2160/21600/3"
                # throwWarning:tr("Missing tag gauge on rail")
                # suggestAlternative:"gauge"
                # -osmoseAssertNoMatchWithContext:list("way railway=disused","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way railway=rail gauge=1435","inside=FR")
                # -osmoseAssertMatchWithContext:list("way railway=rail","inside=FR")
                err.append({'class': 21600, 'subclass': 0, 'text': mapcss.tr('Missing tag gauge on rail')})

        # *[name=~/(?i)co.?voiturage/][amenity][amenity!=car_pooling][!carpool][inside("FR")]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'car_pooling', 'car_pooling')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'carpool')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                # -osmoseAssertNoMatchWithContext:list("way name='Aire de covoiturage' amenity=car_pooling","inside=FR")
                # -osmoseAssertMatchWithContext:list("way name='Aire de covoiturage' amenity=car_sharing","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way name='Aire de covoiturage' amenity=parking carpool=designated","inside=FR")
                # -osmoseAssertNoMatchWithContext:list("way name='Station Covoiturage' public_transport=platform","inside=FR")
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr('Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','car_pooling'],
                    ['carpool','designated']])
                }})

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if ('amenity' in keys and 'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'fuel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, 'yes')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'fuel:e10')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr('Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if ('operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'operator') == mapcss._value_capture(capture_tags, 0, 'ERDF')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['operator','Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if ('ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:ERDF:gdo')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref:FR:gdo', mapcss.tag(tags, 'ref:ERDF:gdo')]]),
                    '-': ([
                    'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if ('ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:gdo')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, '[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if ('operator' in keys and 'power' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'substation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, 'operator'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'switch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 3, tags, 'operator') == mapcss._value_capture(capture_tags, 3, 'Enedis')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if ('ref:FR:ARCEP' in keys) or ('ref:FR:Orange' in keys) or ('ref:FR:PTT' in keys) or ('ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom') != mapcss._value_const_capture(capture_tags, 1, 'connection_point', 'connection_point')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:SFR')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'copper', 'copper')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *["ref:FR:Orange"]["ref:FR:Orange"!~/PT[1-9]{1}[0-9]*/][inside("FR")]
        if ('ref:FR:Orange' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_107d2c86, 'PT[1-9]{1}[0-9]*'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like PT123 without trailing zeros","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like PT123 without trailing zeros', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:Orange:NRO"]["ref:FR:Orange:NRO"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:Orange:NRO' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange:NRO')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange:NRO'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT"]["ref:FR:PTT"!~/[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23d0d993, '[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT:NRA"]["ref:FR:PTT:NRA"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT:NRA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT:NRA')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT:NRA'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/][nat_ref][operator][!junction][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref')) and (mapcss._tag_capture(capture_tags, 2, tags, 'operator')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'junction')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} must be a link road or roundabout","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=primary junction=roundabout nat_ref=62A901609CD_2 operator=SANEF","inside=FR")
                # -osmoseAssertMatchWithContext:list("way highway=primary nat_ref=62A901609CD_2 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} must be a link road or roundabout', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]["nat_ref:backward"][operator][inside("FR")]
        # way[highway=~/^(motorway|trunk|primary|secondary|tertiary)$/]["nat_ref:forward"][operator][inside("FR")]
        if ('highway' in keys and 'nat_ref:backward' in keys and 'operator' in keys) or ('highway' in keys and 'nat_ref:forward' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref:backward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref:forward')) and (mapcss._tag_capture(capture_tags, 2, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} must be a link road ","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref:forward=62A902615CD_1 nat_ref:backward=62A902615CD_2 operator='SANEF'","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} must be a link road ', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][nat_ref!~/^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$/][operator!="VILLE DE PARIS"][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_3863901a, '^([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9])$'), mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'operator') != mapcss._value_const_capture(capture_tags, 3, 'VILLE DE PARIS', 'VILLE DE PARIS')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref=80A901645CD_6 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[junction=roundabout][highway=~/^(motorway|trunk|primary|secondary|tertiary)$/][nat_ref][nat_ref!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        if ('highway' in keys and 'junction' in keys and 'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'junction') == mapcss._value_capture(capture_tags, 0, 'roundabout')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_55ee32ac), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_0c53237c, '^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 3, tags, 'nat_ref'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{2.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=primary junction=roundabout nat_ref=80A901645_6 operator=DIRN","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][nat_ref!~/^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$/][operator="VILLE DE PARIS"][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys and 'operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_6388df2b, '^(75Periph_Paris_[0-9]{2}_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref'))) and (mapcss._tag_capture(capture_tags, 3, tags, 'operator') == mapcss._value_capture(capture_tags, 3, 'VILLE DE PARIS')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference (Paris)","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=trunk_link nat_ref=75Periph_Paris_05_3 operator=\"VILLE DE PARIS\"","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} is not a valid reference (Paris)', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:forward"]["nat_ref:forward"!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        # way[highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:backward"]["nat_ref:backward"!~/^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$/][inside("FR")]
        if ('highway' in keys and 'nat_ref:backward' in keys) or ('highway' in keys and 'nat_ref:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref:forward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_0c53237c, '^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref:forward'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_299ea34e), mapcss._tag_capture(capture_tags, 0, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'nat_ref:backward')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_0c53237c, '^(([1-9][0-9]|0[1-9])[ANP]9[0-9]{3}(|A|N)([0-9]?[0-9]|B1|B2)(|[A-Z]|[a-z])(|CD)_(1[0-9]|[1-9]))$'), mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref:backward'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} is not a valid reference","{1.tag}")
                # -osmoseAssertNoMatchWithContext:list("way highway=motorway_link nat_ref:forward=62A902615CD_1 nat_ref:backward=62A902615CD_2 operator=SANEF","inside=FR")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} is not a valid reference', mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/][nat_ref][!operator][inside("FR")]
        if ('highway' in keys and 'nat_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("Missing tag operator with nat_ref")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('Missing tag operator with nat_ref')})

        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:forward"][!operator][inside("FR")]
        # way[highway][highway=~/^(motorway_link|trunk_link|primary_link|secondary_link|tertiary_link)$/]["nat_ref:backward"][!operator][inside("FR")]
        if ('highway' in keys and 'nat_ref:backward' in keys) or ('highway' in keys and 'nat_ref:forward' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref:forward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'highway')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_299ea34e), mapcss._tag_capture(capture_tags, 1, tags, 'highway'))) and (mapcss._tag_capture(capture_tags, 2, tags, 'nat_ref:backward')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'operator')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("Missing tag operator with nat_ref")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('Missing tag operator with nat_ref')})

        # way.link_road["nat_ref:forward"][oneway=~/^(yes|1|-1)$/][inside("FR")]
        # way.link_road["nat_ref:backward"][oneway=~/^(yes|1|-1)$/][inside("FR")]
        if ('nat_ref:backward' in keys and 'oneway' in keys) or ('nat_ref:forward' in keys and 'oneway' in keys):
            match = False
            # Skip selector using undeclared class link_road
            # Skip selector using undeclared class link_road
            if match:
                # group:tr("validation rules nat_ref in France")
                # -osmoseTags:list("ref","highway")
                # -osmoseItemClassLevel:"9019/9019002/3"
                # throwWarning:tr("{0} no tag forward if oneway","{2.tag}")
                err.append({'class': 9019002, 'subclass': 0, 'text': mapcss.tr('{0} no tag forward if oneway', mapcss._tag_uncapture(capture_tags, '{2.tag}'))})

        # *[amenity=kindergarten][school:FR=maternelle]
        if ('amenity' in keys and 'school:FR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'kindergarten')) and (mapcss._tag_capture(capture_tags, 1, tags, 'school:FR') == mapcss._value_capture(capture_tags, 1, 'maternelle')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misused tag in this country")
                # -osmoseItemClassLevel:"4010/40105/3"
                # throwWarning:"amenity=kindergarten is no longer used for an 'école maternelle' in France, use amenity=school"
                # suggestAlternative:"amenity=school"
                # fixAdd:"amenity=school"
                err.append({'class': 40105, 'subclass': 0, 'text': {'en': 'amenity=kindergarten is no longer used for an \'école maternelle\' in France, use amenity=school'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','school']])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *[name=~/(?i)co.?voiturage/][amenity][amenity!=car_pooling][!carpool][inside("FR")]
        if ('amenity' in keys and 'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_045a0f34), mapcss._tag_capture(capture_tags, 0, tags, 'name'))) and (mapcss._tag_capture(capture_tags, 1, tags, 'amenity')) and (mapcss._tag_capture(capture_tags, 2, tags, 'amenity') != mapcss._value_const_capture(capture_tags, 2, 'car_pooling', 'car_pooling')) and (not mapcss._tag_capture(capture_tags, 3, tags, 'carpool')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"2080/20806/3"
                # throwWarning:tr("Missing tag carpool on area")
                # fixAdd:"amenity=car_pooling"
                # fixAdd:"carpool=designated"
                err.append({'class': 20806, 'subclass': 0, 'text': mapcss.tr('Missing tag carpool on area'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','car_pooling'],
                    ['carpool','designated']])
                }})

        # *[amenity=fuel]["fuel:octane_95"=yes][!"fuel:e10"][inside("FR")]
        if ('amenity' in keys and 'fuel:octane_95' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'fuel')) and (mapcss._tag_capture(capture_tags, 1, tags, 'fuel:octane_95') == mapcss._value_capture(capture_tags, 1, 'yes')) and (not mapcss._tag_capture(capture_tags, 2, tags, 'fuel:e10')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("parking","amenity","fix:chair")
                # -osmoseItemClassLevel:"4061/40612/2"
                # throwWarning:tr("Does this station still sell SP95, or has it been replaced by the SP95-E10?")
                # suggestAlternative:"fuel:e10=yes/no"
                err.append({'class': 40612, 'subclass': 0, 'text': mapcss.tr('Does this station still sell SP95, or has it been replaced by the SP95-E10?')})

        # *[operator=ERDF][inside("FR")]
        if ('operator' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'operator') == mapcss._value_capture(capture_tags, 0, 'ERDF')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("tag","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40103/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"operator=Enedis"
                # fixAdd:"operator=Enedis"
                err.append({'class': 40103, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['operator','Enedis']])
                }})

        # *["ref:ERDF:gdo"][inside("FR")]
        if ('ref:ERDF:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:ERDF:gdo')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("deprecated tagging")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"4010/40104/3"
                # throwWarning:tr("{0} is deprecated","{0.tag}")
                # suggestAlternative:"ref:FR:gdo"
                # fixChangeKey:"ref:ERDF:gdo=>ref:FR:gdo"
                err.append({'class': 40104, 'subclass': 0, 'text': mapcss.tr('{0} is deprecated', mapcss._tag_uncapture(capture_tags, '{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['ref:FR:gdo', mapcss.tag(tags, 'ref:ERDF:gdo')]]),
                    '-': ([
                    'ref:ERDF:gdo'])
                }})

        # *["ref:FR:gdo"]["ref:FR:gdo"!~/[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}/][inside("FR")]
        if ('ref:FR:gdo' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:gdo')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_4bae79a8, '[0-9AB]{5}[A-Z]{1,3}[0-9]{4}|[0-9AB]{5}EEM[0-9]{2}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[power=substation][!"ref:FR:gdo"][ref][operator=~/^(Enedis|GRDF)$/][inside("FR")]
        # *[power=switch][!"ref:FR:gdo"][ref][operator=Enedis][inside("FR")]
        if ('operator' in keys and 'power' in keys and 'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'substation')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss.regexp_test(mapcss._value_capture(capture_tags, 3, self.re_30299d59), mapcss._tag_capture(capture_tags, 3, tags, 'operator'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'power') == mapcss._value_capture(capture_tags, 0, 'switch')) and (not mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:gdo')) and (mapcss._tag_capture(capture_tags, 2, tags, 'ref')) and (mapcss._tag_capture(capture_tags, 3, tags, 'operator') == mapcss._value_capture(capture_tags, 3, 'Enedis')) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","power")
                # -osmoseItemClassLevel:"3040/30402/3"
                # throwWarning:tr("{0} without {1}","{0.tag}","{1.key}")
                err.append({'class': 30402, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.tag}'), mapcss._tag_uncapture(capture_tags, '{1.key}'))})

        # *["ref:FR:ARCEP"][telecom!=connection_point]
        # *["ref:FR:ARCEP"]["telecom:medium"!=fibre]
        # *["ref:FR:Orange"]["telecom:medium"!=fibre]
        # *["ref:FR:SFR"]["telecom:medium"!=fibre]
        # *["ref:FR:PTT"]["telecom:medium"!=copper]
        if ('ref:FR:ARCEP' in keys) or ('ref:FR:Orange' in keys) or ('ref:FR:PTT' in keys) or ('ref:FR:SFR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom') != mapcss._value_const_capture(capture_tags, 1, 'connection_point', 'connection_point')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:ARCEP')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:SFR')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'fibre', 'fibre')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (mapcss._tag_capture(capture_tags, 1, tags, 'telecom:medium') != mapcss._value_const_capture(capture_tags, 1, 'copper', 'copper')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("missing tag")
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30403/3"
                # throwWarning:tr("{0} without {1}","{0.key}","{1.tag}")
                err.append({'class': 30403, 'subclass': 0, 'text': mapcss.tr('{0} without {1}', mapcss._tag_uncapture(capture_tags, '{0.key}'), mapcss._tag_uncapture(capture_tags, '{1.tag}'))})

        # *["ref:FR:Orange"]["ref:FR:Orange"!~/PT[1-9]{1}[0-9]*/][inside("FR")]
        if ('ref:FR:Orange' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_107d2c86, 'PT[1-9]{1}[0-9]*'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like PT123 without trailing zeros","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like PT123 without trailing zeros', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:Orange:NRO"]["ref:FR:Orange:NRO"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:Orange:NRO' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:Orange:NRO')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:Orange:NRO'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT"]["ref:FR:PTT"!~/[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_23d0d993, '[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *["ref:FR:PTT:NRA"]["ref:FR:PTT:NRA"!~/[0-9]{5}[A-Z0-9]{3}/][inside("FR")]
        if ('ref:FR:PTT:NRA' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'ref:FR:PTT:NRA')) and (not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_173ac8d4, '[0-9]{5}[A-Z0-9]{3}'), mapcss._tag_capture(capture_tags, 1, tags, 'ref:FR:PTT:NRA'))) and (mapcss.inside(self.father.config.options, 'FR')))
                except mapcss.RuleAbort: pass
            if match:
                # -osmoseTags:list("ref","infrastructure","telecom")
                # -osmoseItemClassLevel:"3040/30401/3"
                # throwWarning:tr("{0} is invalid. Should look like 12345ABC","{0.tag}")
                err.append({'class': 30401, 'subclass': 0, 'text': mapcss.tr('{0} is invalid. Should look like 12345ABC', mapcss._tag_uncapture(capture_tags, '{0.tag}'))})

        # *[amenity=kindergarten][school:FR=maternelle]
        if ('amenity' in keys and 'school:FR' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = ((mapcss._tag_capture(capture_tags, 0, tags, 'amenity') == mapcss._value_capture(capture_tags, 0, 'kindergarten')) and (mapcss._tag_capture(capture_tags, 1, tags, 'school:FR') == mapcss._value_capture(capture_tags, 1, 'maternelle')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("misused tag in this country")
                # -osmoseItemClassLevel:"4010/40105/3"
                # throwWarning:"amenity=kindergarten is no longer used for an 'école maternelle' in France, use amenity=school"
                # suggestAlternative:"amenity=school"
                # fixAdd:"amenity=school"
                err.append({'class': 40105, 'subclass': 0, 'text': {'en': 'amenity=kindergarten is no longer used for an \'école maternelle\' in France, use amenity=school'}, 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    ['amenity','school']])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_FranceSpecificRules(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}

        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'amenity': 'parking', 'name': 'Aire de Covoiturage'}), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {'distance': '38', 'highway': 'milestone', 'nat_ref': '77PR38DC', 'operator': 'SANEF'}), expected={'class': 30403, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.node(data, {'distance': '38', 'highway': 'milestone', 'nat_ref': '77PR38DC', 'operator': 'SANEF'}), expected={'class': 9019001, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.node(data, {'highway': 'milestone', 'nat_ref': '77PR38DC', 'operator': 'SANEF'}), expected={'class': 9019001, 'subclass': 0})
        self.check_err(n.node(data, {'highway': 'motorway_junction', 'ref': 'N7'}), expected={'class': 9019004, 'subclass': 323412661})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'railway': 'disused'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'gauge': '1435', 'railway': 'rail'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'railway': 'rail'}, [0]), expected={'class': 21600, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'amenity': 'car_pooling', 'name': 'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'amenity': 'car_sharing', 'name': 'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'amenity': 'parking', 'carpool': 'designated', 'name': 'Aire de covoiturage'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'name': 'Station Covoiturage', 'public_transport': 'platform'}, [0]), expected={'class': 20806, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'primary', 'junction': 'roundabout', 'nat_ref': '62A901609CD_2', 'operator': 'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_err(n.way(data, {'highway': 'primary', 'nat_ref': '62A901609CD_2', 'operator': 'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'motorway_link', 'nat_ref:backward': '62A902615CD_2', 'nat_ref:forward': '62A902615CD_1', 'operator': 'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'motorway_link', 'nat_ref': '80A901645CD_6', 'operator': 'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'primary', 'junction': 'roundabout', 'nat_ref': '80A901645_6', 'operator': 'DIRN'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'trunk_link', 'nat_ref': '75Periph_Paris_05_3', 'operator': 'VILLE DE PARIS'}, [0]), expected={'class': 9019002, 'subclass': 0})
        with with_options(n, {'country': 'FR'}):
            self.check_not_err(n.way(data, {'highway': 'motorway_link', 'nat_ref:backward': '62A902615CD_2', 'nat_ref:forward': '62A902615CD_1', 'operator': 'SANEF'}, [0]), expected={'class': 9019002, 'subclass': 0})
