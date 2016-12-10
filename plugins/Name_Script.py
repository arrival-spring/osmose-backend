#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2016                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from plugins.Plugin import Plugin
import regex
import unicodedata


class Name_Script(Plugin):

    def init(self, logger):
        Plugin.init(self, logger)
        self.errors[50701] = { "item": 5070, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Some value chars does not match the language charset") }
        self.errors[50702] = { "item": 5070, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Non printable char") }
        self.errors[50703] = { "item": 5070, "level": 2, "tag": ["name", "fix:chair"], "desc": T_(u"Symbol char") }

        country = self.father.config.options.get("country")

        self.non_printable = regex.compile(u"[\p{Line_Separator}\p{Paragraph_Separator}\p{Control}\p{Private_Use}\p{Surrogate}\p{Unassigned}]", flags=regex.V1)
        # http://unicode.org/cldr/utility/list-unicodeset.jsp?a=[:General_Category=Other_Symbol:]
        self.other_symbol = regex.compile(u"[[\p{General_Category=Other_Symbol}]--[\p{Block=Latin 1 Supplement}\p{Block=Braille Patterns}\p{Block=CJK Radicals Supplement}\p{Block=Kangxi Radicals}\p{Block=CJK Strokes}]--[↔→◄►]]", flags=regex.V1)
        self.non_letter = regex.compile(u"[^\p{Letter}\p{Mark}\p{Separator}]", flags=regex.V1)
        non_look_like_latin = u"\p{Hangul}\p{Bengali}\p{Bopomofo}\p{Braille}\p{Canadian_Aboriginal}\p{Devanagari}\p{Ethiopic}\p{Gujarati}\p{Gurmukhi}\p{Han}\p{Hangul}\p{Hanunoo}\p{Hebrew}\p{Hiragana}\p{Inherited}\p{Kannada}\p{Katakana}\p{Khmer}\p{Lao}\p{Malayalam}\p{Oriya}\p{Runic}\p{Sinhala}\p{Syriac}\p{TaiLe}\p{Tamil}\p{Thaana}\p{Thai}\p{Tibetan}"
        ammend = ""
        if country == "BG":
            ammend = "|TT" # Bulgarian survey point
        self.alone_char = regex.compile(u"(^| |[%s])(?:[A-Z]%s)(?= |[%s]|$)" % (non_look_like_latin, ammend, non_look_like_latin), flags=regex.V1)
        self.roman_number = regex.compile(u"(^| )(?:[IVXLDCM]+)(?= |$)", flags=regex.V1)

        # http://www.regular-expressions.info/unicode.html#script
        # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        self.lang = {
          "ar": u"\p{Arabic}[\u064B-\u064E\u0650-\u0655\u0670]", # u"\p{Arabic}\p{Script_Extensions=Arabic,Syriac}" Arabic,Syriac frequent at least in Iraq,
          "az": u"\p{Arabic}\p{Cyrillic}\p{Latin}",
          "be": u"\p{Cyrillic}",
          "bg": u"\p{Cyrillic}",
          "bn": u"\p{Bengali}",
          "ca": u"\p{Latin}",
          "cs": u"\p{Latin}",
          "da": u"\p{Latin}",
          "de": u"\p{Latin}",
          "dv": None, #Divehi
          "el": u"\p{Greek}",
          "en": u"\p{Latin}",
          "es": u"\p{Latin}",
          "et": u"\p{Latin}",
          "eu": u"\p{Latin}",
          "fa": u"\p{Arabic}[\u064B-\u064E\u0650-\u0655\u0670]", # u"\p{Arabic}\p{Script_Extensions=Arabic,Syriac}",
          "fi": u"\p{Latin}",
          "fo": u"\p{Latin}",
          "fr": u"\p{Latin}",
          "fy": u"\p{Latin}",
          "ga": u"\p{Latin}",
          "gl": u"\p{Latin}",
          "he": u"\p{Hebrew}",
          "hi": u"\p{Devanagari}",
          "hr": u"\p{Latin}",
          "hu": u"\p{Latin}",
          "hy": u"\p{Armenian}",
          "id": u"\p{Latin}",
          "is": u"\p{Latin}",
          "it": u"\p{Latin}",
          "ja": None, # u"\p{Hiragana}\p{Katakana}" and Kanji
          "ka": u"\p{Georgian}",
          "kl": u"\p{Latin}",
          "km": u"\p{Khmer}",
          "ko": u"\p{Hangul}",
          "kw": u"\p{Latin}",
          "lt": u"\p{Latin}",
          "lv": u"\p{Latin}",
          "mg": u"\p{Latin}",
          "mn": None, # Cyrillic + Manchu
          "ms": u"\p{Latin}",
          "my": None, # Birman
          "ne": u"\p{Devanagari}",
          "nl": u"\p{Latin}",
          "no": u"\p{Latin}",
          "pl": u"\p{Latin}",
          "pt": u"\p{Latin}",
          "ro": u"\p{Latin}",
          "ru": u"\p{Cyrillic}",
          "sk": u"\p{Latin}",
          "so": u"\p{Latin}",
          "sq": u"\p{Latin}",
          "sr": u"\p{Cyrillic}",
          "sv": u"\p{Latin}",
          "tg": u"\p{Arabic}\p{Cyrillic}",
          "th": u"\p{Thai}",
          "tk": u"\p{Cyrillic}\p{Latin}",
          "tr": u"\p{Latin}",
          "uk": u"\p{Cyrillic}",
          "vi": u"\p{Latin}",
          "zh": None, # Bopomofo and other
          "zh_TW": None, # Bopomofo and other
        }

        self.default = None
        languages = self.father.config.options.get("language")
        if languages:
            if isinstance(languages, basestring):
                languages = [languages]

            # Assert the languages are mapped to scripts
            for language in languages:
                if language not in self.lang:
                    raise "No script setup for language '%s'" % language

            # Disable default scripts if one language is not mapped to scripts
            for language in languages:
                if not self.lang[language]:
                    languages = None

            # Build default regex
            if languages:
                self.default = regex.compile(r"[\p{Common}%s]" % "".join(map(lambda l: self.lang[l], languages)), flags=regex.V1)

        for l, s in self.lang.items():
            if s == None:
                del(self.lang[l])
            else:
                self.lang[l] = regex.compile(r"[\p{Common}%s]" % s, flags=regex.V1)

        self.names = [u"name", u"name_1", u"name_2", u"alt_name", u"loc_name", u"old_name", u"official_name", u"short_name"]

    def node(self, data, tags):
        err = []
        for key, value in tags.items():
            m = self.non_printable.search(key)
            if m:
                err.append({"class": 50702, "subclass": 0, "text": T_("\"%s\" unexpected non printable char (%s, 0x%04x) in key at position %s", key, unicodedata.name(m.group(0), ''), ord(m.group(0)), m.start() + 1)})
                continue

            m = self.non_printable.search(value)
            if m:
                err.append({"class": 50702, "subclass": 1, "text": T_("\"%s\"=\"%s\" unexpected non printable char (%s, 0x%04x) in value at position %s", key, value, unicodedata.name(m.group(0), ''), ord(m.group(0)), m.start() + 1)})
                continue

            m = self.other_symbol.search(key)
            if m:
                err.append({"class": 50703, "subclass": 0, "text": T_("\"%s\" unexpected symbol char (%s, 0x%04x) in key at position %s", key, unicodedata.name(m.group(0), ''), ord(m.group(0)), m.start() + 1)})
                continue

            m = self.other_symbol.search(value)
            if m:
                err.append({"class": 50703, "subclass": 1, "text": T_("\"%s\"=\"%s\" unexpected symbol char (%s, 0x%04x) in value at position %s", key, value, unicodedata.name(m.group(0), ''), ord(m.group(0)), m.start() + 1)})
                continue

            # https://en.wikipedia.org/wiki/Bi-directional_text#Table_of_possible_BiDi-types
            for c in u"\u200E\u200F\u061C\u202A\u202D\u202B\u202E\u202C\u2066\u2067\u2068\u2069":
                m = key.find(c)
                if m > 0:
                    err.append({"class": 50702, "subclass": 2, "text": T_("\"%s\" unexpected non printable char (%s, 0x%04x) in key at position %s", key, unicodedata.name(c, ''), ord(c), m + 1)})

                m = value.find(c)
                if m > 0:
                    err.append({"class": 50702, "subclass": 2, "text": T_("\"%s\"=\"%s\" unexpected non printable char (%s, 0x%04x) in value at position %s", key, value, unicodedata.name(c, ''), ord(c), m + 1)})

            if self.default:
                if key in self.names:
                    s = self.non_letter.sub(u" ", value)
                    s = self.alone_char.sub(u"", s)
                    s = self.roman_number.sub(u"", s)
                    s = self.default.sub(u"", s)
                    if len(s) > 0 and \
                        not(len(value) == 2 and len(s) == 1) and \
                        len(s) <= len(value) / 10 + 1:
                        if len(s) == 1:
                            err.append({"class": 50701, "subclass": 0, "text": T_("\"%s\"=\"%s\" unexpected char \"%s\" (%s, 0x%04x)", key, value, s, unicodedata.name(s[0], ''), ord(s[0]))})
                        else:
                            err.append({"class": 50701, "subclass": 0, "text": T_("\"%s\"=\"%s\" unexpected \"%s\"", key, value, s)})

            l = key.split(':')
            if len(l) > 1 and l[0] in self.names and l[1] in self.lang:
                s = self.non_letter.sub(u" ", value)
                s = self.alone_char.sub(u"\\1", s)
                s = self.roman_number.sub(u"\\1", s)
                s = self.lang[l[1]].sub(u"", s)
                if len(s) > 0:
                    if len(s) == 1:
                        err.append({"class": 50701, "subclass": 1, "text": T_("\"%s\"=\"%s\" unexpected char \"%s\" (%s, 0x%04x)", key, value, s, unicodedata.name(s[0], ''), ord(s[0]))})
                    else:
                        err.append({"class": 50701, "subclass": 1, "text": T_("\"%s\"=\"%s\" unexpected \"%s\"", key, value, s)})

        return err

    def way(self, data, tags, nds):
        return self.node(data, tags)

    def relation(self, data, tags, members):
        return self.node(data, tags)


###########################################################################
from plugins.Plugin import TestPluginCommon

class Test(TestPluginCommon):
    def test_(self):
        a = Name_Script(None)
        class _config:
            options = {"country": "FR"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {u"name": u"test ь"})
        assert not a.node(None, {u"name": u"Sacré-Cœur"})

        self.check_err(a.node(None, {u"name:uk": u"Sacré-Cœur"}))

    def test_fr(self):
        a = Name_Script(None)
        class _config:
            options = {"language": "fr"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {u"seamark:light:information": u"R. 340° -095° , W.-111° , G.-160°"})
        assert not a.node(None, {u"source": u"©IGN 2010"})
        assert not a.node(None, {u"name": u"Karditsa → Larisa"})
        assert not a.node(None, {u"name": u"To Embonas ►"})

        self.check_err(a.node(None, {u"name": u"test ь"}))
        self.check_err(a.node(None, {u"name": u"🇮🇶🏠"}))
        assert not a.node(None, {u"name": u"test кодувань"})
        assert not a.node(None, {u"name": u"кодувань"})
        assert not a.node(None, {u"name": u"Sophie II"})
        assert not a.node(None, {u"name": u"Sacré-Cœur"})
        assert not a.node(None, {u"name": u"дA"})

        assert not a.node(None, {u"name:uk": u"кодувань"})
        assert not a.node(None, {u"name:tg": u"Париж"})
        self.check_err(a.node(None, {u"name:uk": u"Sacré-Cœur"}))
        assert not a.node(None, {u"name:uk": u"кодувань A"})
        assert not a.node(None, {u"name:uk": u"кодувань A33"})
        assert not a.node(None, {u"name:uk": u"B2"})
        assert not a.node(None, {u"name:el": u"Διαδρομος 15R/33L"})
        self.check_err(a.node(None, {u"name:el": u"ροMμος"}))
        assert not a.node(None, {u"name:fa": u"شیب دِراز"})
        assert not a.node(None, {u"name:th": u"P T L"})
        self.check_err(a.node(None, {u"name:ru": u"Кари́бские Нидерла́нды"}))
        assert not a.node(None, {u"name:ar": u"مسكّن عدي"})
        assert not a.node(None, {u"name:ko": u"유스페이스2 B동"})

    def test_fr_nl(self):
        a = Name_Script(None)
        class _config:
            options = {"language": ["fr", "nl"]}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        self.check_err(a.node(None, {u"name": u"test ь"}))
        assert not a.node(None, {u"name": u"test кодувань"})

        assert not a.node(None, {u"name:uk": u"кодувань"})
        self.check_err(a.node(None, {u"name:uk": u"Sacré-Cœur"}))

    def test_zh(self):
        a = Name_Script(None)
        class _config:
            options = {"language": "zh"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {u"name": u"test ь"})
        assert not a.node(None, {u"name": u"test кодувань"})

        assert not a.node(None, {u"name:uk": u"кодувань"})
        self.check_err(a.node(None, {u"name:uk": u"Sacré-Cœur"}))

    def test_BG(self):
        a = Name_Script(None)
        class _config:
            options = {"language": "bg", "country": "BG"}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        assert not a.node(None, {u"name": u"TT190/XXVI/"}) # Bulgarian survey point

    def test_non_printable(self):
        a = Name_Script(None)
        class _config:
            options = {}
        class father:
            config = _config()
        a.father = father()
        a.init(None)

        self.check_err(a.node(None, {u"name\u0001": u"test"}))
        self.check_err(a.node(None, {u"name": u"test \u0000"}))
        self.check_err(a.node(None, {u"name": u"test \u202B"}))
