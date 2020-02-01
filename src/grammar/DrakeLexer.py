# Generated from Drake.g4 by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


from antlr4.Token import CommonToken
import re
import importlib

# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2c")
        buf.write("\u0372\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT\4U\t")
        buf.write("U\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4")
        buf.write("^\t^\4_\t_\4`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4")
        buf.write("g\tg\4h\th\4i\ti\4j\tj\4k\tk\4l\tl\4m\tm\4n\tn\4o\to\4")
        buf.write("p\tp\4q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4w\tw\4x\tx\4")
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\3\2\3\2\3\2\3\2\3\3\3\3\5")
        buf.write("\3\u0102\n\3\3\4\3\4\3\4\3\4\5\4\u0108\n\4\3\5\3\5\3\5")
        buf.write("\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3")
        buf.write("\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\n")
        buf.write("\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write("\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20")
        buf.write("\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22")
        buf.write("\3\22\3\23\3\23\3\23\3\24\3\24\3\24\3\24\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30")
        buf.write("\3\30\3\30\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\33\3\33")
        buf.write("\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\35\3\36")
        buf.write("\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3\37\3 ")
        buf.write("\3 \3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3#\3")
        buf.write("#\3#\3#\3#\3$\3$\3$\3$\3$\3$\3$\3$\3$\3%\3%\3%\3%\3%\3")
        buf.write("%\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\5")
        buf.write("(\u01cb\n(\3(\3(\5(\u01cf\n(\3(\5(\u01d2\n(\5(\u01d4\n")
        buf.write("(\3(\3(\3)\3)\7)\u01da\n)\f)\16)\u01dd\13)\3*\3*\3*\3")
        buf.write("*\3*\5*\u01e4\n*\3*\3*\5*\u01e8\n*\3+\3+\3+\3+\3+\5+\u01ef")
        buf.write("\n+\3+\3+\5+\u01f3\n+\3,\3,\7,\u01f7\n,\f,\16,\u01fa\13")
        buf.write(",\3,\6,\u01fd\n,\r,\16,\u01fe\5,\u0201\n,\3-\3-\3-\6-")
        buf.write("\u0206\n-\r-\16-\u0207\3.\3.\3.\6.\u020d\n.\r.\16.\u020e")
        buf.write("\3/\3/\3/\6/\u0214\n/\r/\16/\u0215\3\60\3\60\5\60\u021a")
        buf.write("\n\60\3\61\3\61\5\61\u021e\n\61\3\61\3\61\3\62\3\62\3")
        buf.write("\63\3\63\3\63\3\63\3\64\3\64\3\65\3\65\3\65\3\66\3\66")
        buf.write("\3\66\3\67\3\67\38\38\39\39\3:\3:\3:\3;\3;\3<\3<\3<\3")
        buf.write("=\3=\3=\3>\3>\3?\3?\3@\3@\3A\3A\3A\3B\3B\3B\3C\3C\3D\3")
        buf.write("D\3E\3E\3F\3F\3G\3G\3G\3H\3H\3I\3I\3I\3J\3J\3J\3K\3K\3")
        buf.write("L\3L\3M\3M\3M\3N\3N\3N\3O\3O\3O\3P\3P\3P\3Q\3Q\3Q\3R\3")
        buf.write("R\3S\3S\3S\3T\3T\3T\3U\3U\3U\3V\3V\3V\3W\3W\3W\3X\3X\3")
        buf.write("X\3Y\3Y\3Y\3Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3]\3]\3]\3]\3")
        buf.write("^\3^\3^\3^\3_\3_\3_\3_\3`\3`\3`\3`\3a\3a\3a\5a\u02a6\n")
        buf.write("a\3a\3a\3b\3b\3c\3c\3c\7c\u02af\nc\fc\16c\u02b2\13c\3")
        buf.write("c\3c\3c\3c\7c\u02b8\nc\fc\16c\u02bb\13c\3c\5c\u02be\n")
        buf.write("c\3d\3d\3d\3d\3d\7d\u02c5\nd\fd\16d\u02c8\13d\3d\3d\3")
        buf.write("d\3d\3d\3d\3d\3d\7d\u02d2\nd\fd\16d\u02d5\13d\3d\3d\3")
        buf.write("d\5d\u02da\nd\3e\3e\5e\u02de\ne\3f\3f\3g\3g\3g\3g\5g\u02e6")
        buf.write("\ng\3h\3h\3i\3i\3j\3j\3k\3k\3l\3l\3m\5m\u02f3\nm\3m\3")
        buf.write("m\3m\3m\5m\u02f9\nm\3n\3n\5n\u02fd\nn\3n\3n\3o\6o\u0302")
        buf.write("\no\ro\16o\u0303\3p\3p\6p\u0308\np\rp\16p\u0309\3q\3q")
        buf.write("\5q\u030e\nq\3q\6q\u0311\nq\rq\16q\u0312\3r\3r\3r\7r\u0318")
        buf.write("\nr\fr\16r\u031b\13r\3r\3r\3r\3r\7r\u0321\nr\fr\16r\u0324")
        buf.write("\13r\3r\5r\u0327\nr\3s\3s\3s\3s\3s\7s\u032e\ns\fs\16s")
        buf.write("\u0331\13s\3s\3s\3s\3s\3s\3s\3s\3s\7s\u033b\ns\fs\16s")
        buf.write("\u033e\13s\3s\3s\3s\5s\u0343\ns\3t\3t\5t\u0347\nt\3u\5")
        buf.write("u\u034a\nu\3v\5v\u034d\nv\3w\5w\u0350\nw\3x\3x\3x\3y\6")
        buf.write("y\u0356\ny\ry\16y\u0357\3z\3z\7z\u035c\nz\fz\16z\u035f")
        buf.write("\13z\3{\3{\5{\u0363\n{\3{\5{\u0366\n{\3{\3{\5{\u036a\n")
        buf.write("{\3|\5|\u036d\n|\3}\3}\5}\u0371\n}\6\u02c6\u02d3\u032f")
        buf.write("\u033c\2~\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25")
        buf.write("\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+")
        buf.write("\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E")
        buf.write("$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k")
        buf.write("\67m8o9q:s;u<w=y>{?}@\177A\u0081B\u0083C\u0085D\u0087")
        buf.write("E\u0089F\u008bG\u008dH\u008fI\u0091J\u0093K\u0095L\u0097")
        buf.write("M\u0099N\u009bO\u009dP\u009fQ\u00a1R\u00a3S\u00a5T\u00a7")
        buf.write("U\u00a9V\u00abW\u00adX\u00afY\u00b1Z\u00b3[\u00b5\\\u00b7")
        buf.write("]\u00b9^\u00bb_\u00bd`\u00bfa\u00c1b\u00c3c\u00c5\2\u00c7")
        buf.write("\2\u00c9\2\u00cb\2\u00cd\2\u00cf\2\u00d1\2\u00d3\2\u00d5")
        buf.write("\2\u00d7\2\u00d9\2\u00db\2\u00dd\2\u00df\2\u00e1\2\u00e3")
        buf.write("\2\u00e5\2\u00e7\2\u00e9\2\u00eb\2\u00ed\2\u00ef\2\u00f1")
        buf.write("\2\u00f3\2\u00f5\2\u00f7\2\u00f9\2\3\2\33\b\2HHTTWWhh")
        buf.write("ttww\4\2HHhh\4\2TTtt\4\2DDdd\4\2QQqq\4\2ZZzz\4\2LLll\6")
        buf.write("\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\3\2^^\3\2\63;\3\2\62")
        buf.write(";\3\2\629\5\2\62;CHch\3\2\62\63\4\2GGgg\4\2--//\7\2\2")
        buf.write("\13\r\16\20(*]_\u0081\7\2\2\13\r\16\20#%]_\u0081\4\2\2")
        buf.write("]_\u0081\3\2\2\u0081\4\2\13\13\"\"\4\2\f\f\16\17\u0129")
        buf.write("\2C\\aac|\u00ac\u00ac\u00b7\u00b7\u00bc\u00bc\u00c2\u00d8")
        buf.write("\u00da\u00f8\u00fa\u0243\u0252\u02c3\u02c8\u02d3\u02e2")
        buf.write("\u02e6\u02f0\u02f0\u037c\u037c\u0388\u0388\u038a\u038c")
        buf.write("\u038e\u038e\u0390\u03a3\u03a5\u03d0\u03d2\u03f7\u03f9")
        buf.write("\u0483\u048c\u04d0\u04d2\u04fb\u0502\u0511\u0533\u0558")
        buf.write("\u055b\u055b\u0563\u0589\u05d2\u05ec\u05f2\u05f4\u0623")
        buf.write("\u063c\u0642\u064c\u0670\u0671\u0673\u06d5\u06d7\u06d7")
        buf.write("\u06e7\u06e8\u06f0\u06f1\u06fc\u06fe\u0701\u0701\u0712")
        buf.write("\u0712\u0714\u0731\u074f\u076f\u0782\u07a7\u07b3\u07b3")
        buf.write("\u0906\u093b\u093f\u093f\u0952\u0952\u095a\u0963\u097f")
        buf.write("\u097f\u0987\u098e\u0991\u0992\u0995\u09aa\u09ac\u09b2")
        buf.write("\u09b4\u09b4\u09b8\u09bb\u09bf\u09bf\u09d0\u09d0\u09de")
        buf.write("\u09df\u09e1\u09e3\u09f2\u09f3\u0a07\u0a0c\u0a11\u0a12")
        buf.write("\u0a15\u0a2a\u0a2c\u0a32\u0a34\u0a35\u0a37\u0a38\u0a3a")
        buf.write("\u0a3b\u0a5b\u0a5e\u0a60\u0a60\u0a74\u0a76\u0a87\u0a8f")
        buf.write("\u0a91\u0a93\u0a95\u0aaa\u0aac\u0ab2\u0ab4\u0ab5\u0ab7")
        buf.write("\u0abb\u0abf\u0abf\u0ad2\u0ad2\u0ae2\u0ae3\u0b07\u0b0e")
        buf.write("\u0b11\u0b12\u0b15\u0b2a\u0b2c\u0b32\u0b34\u0b35\u0b37")
        buf.write("\u0b3b\u0b3f\u0b3f\u0b5e\u0b5f\u0b61\u0b63\u0b73\u0b73")
        buf.write("\u0b85\u0b85\u0b87\u0b8c\u0b90\u0b92\u0b94\u0b97\u0b9b")
        buf.write("\u0b9c\u0b9e\u0b9e\u0ba0\u0ba1\u0ba5\u0ba6\u0baa\u0bac")
        buf.write("\u0bb0\u0bbb\u0c07\u0c0e\u0c10\u0c12\u0c14\u0c2a\u0c2c")
        buf.write("\u0c35\u0c37\u0c3b\u0c62\u0c63\u0c87\u0c8e\u0c90\u0c92")
        buf.write("\u0c94\u0caa\u0cac\u0cb5\u0cb7\u0cbb\u0cbf\u0cbf\u0ce0")
        buf.write("\u0ce0\u0ce2\u0ce3\u0d07\u0d0e\u0d10\u0d12\u0d14\u0d2a")
        buf.write("\u0d2c\u0d3b\u0d62\u0d63\u0d87\u0d98\u0d9c\u0db3\u0db5")
        buf.write("\u0dbd\u0dbf\u0dbf\u0dc2\u0dc8\u0e03\u0e32\u0e34\u0e35")
        buf.write("\u0e42\u0e48\u0e83\u0e84\u0e86\u0e86\u0e89\u0e8a\u0e8c")
        buf.write("\u0e8c\u0e8f\u0e8f\u0e96\u0e99\u0e9b\u0ea1\u0ea3\u0ea5")
        buf.write("\u0ea7\u0ea7\u0ea9\u0ea9\u0eac\u0ead\u0eaf\u0eb2\u0eb4")
        buf.write("\u0eb5\u0ebf\u0ebf\u0ec2\u0ec6\u0ec8\u0ec8\u0ede\u0edf")
        buf.write("\u0f02\u0f02\u0f42\u0f49\u0f4b\u0f6c\u0f8a\u0f8d\u1002")
        buf.write("\u1023\u1025\u1029\u102b\u102c\u1052\u1057\u10a2\u10c7")
        buf.write("\u10d2\u10fc\u10fe\u10fe\u1102\u115b\u1161\u11a4\u11aa")
        buf.write("\u11fb\u1202\u124a\u124c\u124f\u1252\u1258\u125a\u125a")
        buf.write("\u125c\u125f\u1262\u128a\u128c\u128f\u1292\u12b2\u12b4")
        buf.write("\u12b7\u12ba\u12c0\u12c2\u12c2\u12c4\u12c7\u12ca\u12d8")
        buf.write("\u12da\u1312\u1314\u1317\u131a\u135c\u1382\u1391\u13a2")
        buf.write("\u13f6\u1403\u166e\u1671\u1678\u1683\u169c\u16a2\u16ec")
        buf.write("\u16f0\u16f2\u1702\u170e\u1710\u1713\u1722\u1733\u1742")
        buf.write("\u1753\u1762\u176e\u1770\u1772\u1782\u17b5\u17d9\u17d9")
        buf.write("\u17de\u17de\u1822\u1879\u1882\u18aa\u1902\u191e\u1952")
        buf.write("\u196f\u1972\u1976\u1982\u19ab\u19c3\u19c9\u1a02\u1a18")
        buf.write("\u1d02\u1dc1\u1e02\u1e9d\u1ea2\u1efb\u1f02\u1f17\u1f1a")
        buf.write("\u1f1f\u1f22\u1f47\u1f4a\u1f4f\u1f52\u1f59\u1f5b\u1f5b")
        buf.write("\u1f5d\u1f5d\u1f5f\u1f5f\u1f61\u1f7f\u1f82\u1fb6\u1fb8")
        buf.write("\u1fbe\u1fc0\u1fc0\u1fc4\u1fc6\u1fc8\u1fce\u1fd2\u1fd5")
        buf.write("\u1fd8\u1fdd\u1fe2\u1fee\u1ff4\u1ff6\u1ff8\u1ffe\u2073")
        buf.write("\u2073\u2081\u2081\u2092\u2096\u2104\u2104\u2109\u2109")
        buf.write("\u210c\u2115\u2117\u2117\u211a\u211f\u2126\u2126\u2128")
        buf.write("\u2128\u212a\u212a\u212c\u2133\u2135\u213b\u213e\u2141")
        buf.write("\u2147\u214b\u2162\u2185\u2c02\u2c30\u2c32\u2c60\u2c82")
        buf.write("\u2ce6\u2d02\u2d27\u2d32\u2d67\u2d71\u2d71\u2d82\u2d98")
        buf.write("\u2da2\u2da8\u2daa\u2db0\u2db2\u2db8\u2dba\u2dc0\u2dc2")
        buf.write("\u2dc8\u2dca\u2dd0\u2dd2\u2dd8\u2dda\u2de0\u3007\u3009")
        buf.write("\u3023\u302b\u3033\u3037\u303a\u303e\u3043\u3098\u309d")
        buf.write("\u30a1\u30a3\u30fc\u30fe\u3101\u3107\u312e\u3133\u3190")
        buf.write("\u31a2\u31b9\u31f2\u3201\u3402\u4db7\u4e02\u9fbd\ua002")
        buf.write("\ua48e\ua802\ua803\ua805\ua807\ua809\ua80c\ua80e\ua824")
        buf.write("\uac02\ud7a5\uf902\ufa2f\ufa32\ufa6c\ufa72\ufadb\ufb02")
        buf.write("\ufb08\ufb15\ufb19\ufb1f\ufb1f\ufb21\ufb2a\ufb2c\ufb38")
        buf.write("\ufb3a\ufb3e\ufb40\ufb40\ufb42\ufb43\ufb45\ufb46\ufb48")
        buf.write("\ufbb3\ufbd5\ufd3f\ufd52\ufd91\ufd94\ufdc9\ufdf2\ufdfd")
        buf.write("\ufe72\ufe76\ufe78\ufefe\uff23\uff3c\uff43\uff5c\uff68")
        buf.write("\uffc0\uffc4\uffc9\uffcc\uffd1\uffd4\uffd9\uffdc\uffde")
        buf.write("\u0096\2\62;\u0302\u0371\u0485\u0488\u0593\u05bb\u05bd")
        buf.write("\u05bf\u05c1\u05c1\u05c3\u05c4\u05c6\u05c7\u05c9\u05c9")
        buf.write("\u0612\u0617\u064d\u0660\u0662\u066b\u0672\u0672\u06d8")
        buf.write("\u06de\u06e1\u06e6\u06e9\u06ea\u06ec\u06ef\u06f2\u06fb")
        buf.write("\u0713\u0713\u0732\u074c\u07a8\u07b2\u0903\u0905\u093e")
        buf.write("\u093e\u0940\u094f\u0953\u0956\u0964\u0965\u0968\u0971")
        buf.write("\u0983\u0985\u09be\u09be\u09c0\u09c6\u09c9\u09ca\u09cd")
        buf.write("\u09cf\u09d9\u09d9\u09e4\u09e5\u09e8\u09f1\u0a03\u0a05")
        buf.write("\u0a3e\u0a3e\u0a40\u0a44\u0a49\u0a4a\u0a4d\u0a4f\u0a68")
        buf.write("\u0a73\u0a83\u0a85\u0abe\u0abe\u0ac0\u0ac7\u0ac9\u0acb")
        buf.write("\u0acd\u0acf\u0ae4\u0ae5\u0ae8\u0af1\u0b03\u0b05\u0b3e")
        buf.write("\u0b3e\u0b40\u0b45\u0b49\u0b4a\u0b4d\u0b4f\u0b58\u0b59")
        buf.write("\u0b68\u0b71\u0b84\u0b84\u0bc0\u0bc4\u0bc8\u0bca\u0bcc")
        buf.write("\u0bcf\u0bd9\u0bd9\u0be8\u0bf1\u0c03\u0c05\u0c40\u0c46")
        buf.write("\u0c48\u0c4a\u0c4c\u0c4f\u0c57\u0c58\u0c68\u0c71\u0c84")
        buf.write("\u0c85\u0cbe\u0cbe\u0cc0\u0cc6\u0cc8\u0cca\u0ccc\u0ccf")
        buf.write("\u0cd7\u0cd8\u0ce8\u0cf1\u0d04\u0d05\u0d40\u0d45\u0d48")
        buf.write("\u0d4a\u0d4c\u0d4f\u0d59\u0d59\u0d68\u0d71\u0d84\u0d85")
        buf.write("\u0dcc\u0dcc\u0dd1\u0dd6\u0dd8\u0dd8\u0dda\u0de1\u0df4")
        buf.write("\u0df5\u0e33\u0e33\u0e36\u0e3c\u0e49\u0e50\u0e52\u0e5b")
        buf.write("\u0eb3\u0eb3\u0eb6\u0ebb\u0ebd\u0ebe\u0eca\u0ecf\u0ed2")
        buf.write("\u0edb\u0f1a\u0f1b\u0f22\u0f2b\u0f37\u0f37\u0f39\u0f39")
        buf.write("\u0f3b\u0f3b\u0f40\u0f41\u0f73\u0f86\u0f88\u0f89\u0f92")
        buf.write("\u0f99\u0f9b\u0fbe\u0fc8\u0fc8\u102e\u1034\u1038\u103b")
        buf.write("\u1042\u104b\u1058\u105b\u1361\u1361\u136b\u1373\u1714")
        buf.write("\u1716\u1734\u1736\u1754\u1755\u1774\u1775\u17b8\u17d5")
        buf.write("\u17df\u17df\u17e2\u17eb\u180d\u180f\u1812\u181b\u18ab")
        buf.write("\u18ab\u1922\u192d\u1932\u193d\u1948\u1951\u19b2\u19c2")
        buf.write("\u19ca\u19cb\u19d2\u19db\u1a19\u1a1d\u1dc2\u1dc5\u2041")
        buf.write("\u2042\u2056\u2056\u20d2\u20de\u20e3\u20e3\u20e7\u20ed")
        buf.write("\u302c\u3031\u309b\u309c\ua804\ua804\ua808\ua808\ua80d")
        buf.write("\ua80d\ua825\ua829\ufb20\ufb20\ufe02\ufe11\ufe22\ufe25")
        buf.write("\ufe35\ufe36\ufe4f\ufe51\uff12\uff1b\uff41\uff41\2\u0390")
        buf.write("\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13")
        buf.write("\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3")
        buf.write("\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2")
        buf.write("\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2")
        buf.write("%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2")
        buf.write("\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67")
        buf.write("\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2")
        buf.write("A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2")
        buf.write("\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2")
        buf.write("\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2")
        buf.write("\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3")
        buf.write("\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q")
        buf.write("\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2")
        buf.write("{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083")
        buf.write("\3\2\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2")
        buf.write("\2\2\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2")
        buf.write("\2\2\u00c3\3\2\2\2\3\u00fb\3\2\2\2\5\u0101\3\2\2\2\7\u0107")
        buf.write("\3\2\2\2\t\u0109\3\2\2\2\13\u010d\3\2\2\2\r\u0114\3\2")
        buf.write("\2\2\17\u011a\3\2\2\2\21\u011f\3\2\2\2\23\u0126\3\2\2")
        buf.write("\2\25\u0129\3\2\2\2\27\u0130\3\2\2\2\31\u0139\3\2\2\2")
        buf.write("\33\u0140\3\2\2\2\35\u0143\3\2\2\2\37\u0148\3\2\2\2!\u014d")
        buf.write("\3\2\2\2#\u0153\3\2\2\2%\u0157\3\2\2\2\'\u015a\3\2\2\2")
        buf.write(")\u015e\3\2\2\2+\u0166\3\2\2\2-\u016b\3\2\2\2/\u0172\3")
        buf.write("\2\2\2\61\u0179\3\2\2\2\63\u017c\3\2\2\2\65\u0180\3\2")
        buf.write("\2\2\67\u0184\3\2\2\29\u0187\3\2\2\2;\u018c\3\2\2\2=\u0191")
        buf.write("\3\2\2\2?\u0197\3\2\2\2A\u019d\3\2\2\2C\u01a3\3\2\2\2")
        buf.write("E\u01a7\3\2\2\2G\u01ac\3\2\2\2I\u01b5\3\2\2\2K\u01bb\3")
        buf.write("\2\2\2M\u01c1\3\2\2\2O\u01d3\3\2\2\2Q\u01d7\3\2\2\2S\u01e3")
        buf.write("\3\2\2\2U\u01ee\3\2\2\2W\u0200\3\2\2\2Y\u0202\3\2\2\2")
        buf.write("[\u0209\3\2\2\2]\u0210\3\2\2\2_\u0219\3\2\2\2a\u021d\3")
        buf.write("\2\2\2c\u0221\3\2\2\2e\u0223\3\2\2\2g\u0227\3\2\2\2i\u0229")
        buf.write("\3\2\2\2k\u022c\3\2\2\2m\u022f\3\2\2\2o\u0231\3\2\2\2")
        buf.write("q\u0233\3\2\2\2s\u0235\3\2\2\2u\u0238\3\2\2\2w\u023a\3")
        buf.write("\2\2\2y\u023d\3\2\2\2{\u0240\3\2\2\2}\u0242\3\2\2\2\177")
        buf.write("\u0244\3\2\2\2\u0081\u0246\3\2\2\2\u0083\u0249\3\2\2\2")
        buf.write("\u0085\u024c\3\2\2\2\u0087\u024e\3\2\2\2\u0089\u0250\3")
        buf.write("\2\2\2\u008b\u0252\3\2\2\2\u008d\u0254\3\2\2\2\u008f\u0257")
        buf.write("\3\2\2\2\u0091\u0259\3\2\2\2\u0093\u025c\3\2\2\2\u0095")
        buf.write("\u025f\3\2\2\2\u0097\u0261\3\2\2\2\u0099\u0263\3\2\2\2")
        buf.write("\u009b\u0266\3\2\2\2\u009d\u0269\3\2\2\2\u009f\u026c\3")
        buf.write("\2\2\2\u00a1\u026f\3\2\2\2\u00a3\u0272\3\2\2\2\u00a5\u0274")
        buf.write("\3\2\2\2\u00a7\u0277\3\2\2\2\u00a9\u027a\3\2\2\2\u00ab")
        buf.write("\u027d\3\2\2\2\u00ad\u0280\3\2\2\2\u00af\u0283\3\2\2\2")
        buf.write("\u00b1\u0286\3\2\2\2\u00b3\u0289\3\2\2\2\u00b5\u028c\3")
        buf.write("\2\2\2\u00b7\u028f\3\2\2\2\u00b9\u0292\3\2\2\2\u00bb\u0296")
        buf.write("\3\2\2\2\u00bd\u029a\3\2\2\2\u00bf\u029e\3\2\2\2\u00c1")
        buf.write("\u02a5\3\2\2\2\u00c3\u02a9\3\2\2\2\u00c5\u02bd\3\2\2\2")
        buf.write("\u00c7\u02d9\3\2\2\2\u00c9\u02dd\3\2\2\2\u00cb\u02df\3")
        buf.write("\2\2\2\u00cd\u02e5\3\2\2\2\u00cf\u02e7\3\2\2\2\u00d1\u02e9")
        buf.write("\3\2\2\2\u00d3\u02eb\3\2\2\2\u00d5\u02ed\3\2\2\2\u00d7")
        buf.write("\u02ef\3\2\2\2\u00d9\u02f8\3\2\2\2\u00db\u02fc\3\2\2\2")
        buf.write("\u00dd\u0301\3\2\2\2\u00df\u0305\3\2\2\2\u00e1\u030b\3")
        buf.write("\2\2\2\u00e3\u0326\3\2\2\2\u00e5\u0342\3\2\2\2\u00e7\u0346")
        buf.write("\3\2\2\2\u00e9\u0349\3\2\2\2\u00eb\u034c\3\2\2\2\u00ed")
        buf.write("\u034f\3\2\2\2\u00ef\u0351\3\2\2\2\u00f1\u0355\3\2\2\2")
        buf.write("\u00f3\u0359\3\2\2\2\u00f5\u0360\3\2\2\2\u00f7\u036c\3")
        buf.write("\2\2\2\u00f9\u0370\3\2\2\2\u00fb\u00fc\7k\2\2\u00fc\u00fd")
        buf.write("\7u\2\2\u00fd\u00fe\7c\2\2\u00fe\4\3\2\2\2\u00ff\u0102")
        buf.write("\5S*\2\u0100\u0102\5U+\2\u0101\u00ff\3\2\2\2\u0101\u0100")
        buf.write("\3\2\2\2\u0102\6\3\2\2\2\u0103\u0108\5W,\2\u0104\u0108")
        buf.write("\5Y-\2\u0105\u0108\5[.\2\u0106\u0108\5]/\2\u0107\u0103")
        buf.write("\3\2\2\2\u0107\u0104\3\2\2\2\u0107\u0105\3\2\2\2\u0107")
        buf.write("\u0106\3\2\2\2\u0108\b\3\2\2\2\u0109\u010a\7f\2\2\u010a")
        buf.write("\u010b\7g\2\2\u010b\u010c\7h\2\2\u010c\n\3\2\2\2\u010d")
        buf.write("\u010e\7t\2\2\u010e\u010f\7g\2\2\u010f\u0110\7v\2\2\u0110")
        buf.write("\u0111\7w\2\2\u0111\u0112\7t\2\2\u0112\u0113\7p\2\2\u0113")
        buf.write("\f\3\2\2\2\u0114\u0115\7t\2\2\u0115\u0116\7c\2\2\u0116")
        buf.write("\u0117\7k\2\2\u0117\u0118\7u\2\2\u0118\u0119\7g\2\2\u0119")
        buf.write("\16\3\2\2\2\u011a\u011b\7h\2\2\u011b\u011c\7t\2\2\u011c")
        buf.write("\u011d\7q\2\2\u011d\u011e\7o\2\2\u011e\20\3\2\2\2\u011f")
        buf.write("\u0120\7k\2\2\u0120\u0121\7o\2\2\u0121\u0122\7r\2\2\u0122")
        buf.write("\u0123\7q\2\2\u0123\u0124\7t\2\2\u0124\u0125\7v\2\2\u0125")
        buf.write("\22\3\2\2\2\u0126\u0127\7c\2\2\u0127\u0128\7u\2\2\u0128")
        buf.write("\24\3\2\2\2\u0129\u012a\7i\2\2\u012a\u012b\7n\2\2\u012b")
        buf.write("\u012c\7q\2\2\u012c\u012d\7d\2\2\u012d\u012e\7c\2\2\u012e")
        buf.write("\u012f\7n\2\2\u012f\26\3\2\2\2\u0130\u0131\7p\2\2\u0131")
        buf.write("\u0132\7q\2\2\u0132\u0133\7p\2\2\u0133\u0134\7n\2\2\u0134")
        buf.write("\u0135\7q\2\2\u0135\u0136\7e\2\2\u0136\u0137\7c\2\2\u0137")
        buf.write("\u0138\7n\2\2\u0138\30\3\2\2\2\u0139\u013a\7c\2\2\u013a")
        buf.write("\u013b\7u\2\2\u013b\u013c\7u\2\2\u013c\u013d\7g\2\2\u013d")
        buf.write("\u013e\7t\2\2\u013e\u013f\7v\2\2\u013f\32\3\2\2\2\u0140")
        buf.write("\u0141\7k\2\2\u0141\u0142\7h\2\2\u0142\34\3\2\2\2\u0143")
        buf.write("\u0144\7g\2\2\u0144\u0145\7n\2\2\u0145\u0146\7k\2\2\u0146")
        buf.write("\u0147\7h\2\2\u0147\36\3\2\2\2\u0148\u0149\7g\2\2\u0149")
        buf.write("\u014a\7n\2\2\u014a\u014b\7u\2\2\u014b\u014c\7g\2\2\u014c")
        buf.write(" \3\2\2\2\u014d\u014e\7y\2\2\u014e\u014f\7j\2\2\u014f")
        buf.write("\u0150\7k\2\2\u0150\u0151\7n\2\2\u0151\u0152\7g\2\2\u0152")
        buf.write("\"\3\2\2\2\u0153\u0154\7h\2\2\u0154\u0155\7q\2\2\u0155")
        buf.write("\u0156\7t\2\2\u0156$\3\2\2\2\u0157\u0158\7k\2\2\u0158")
        buf.write("\u0159\7p\2\2\u0159&\3\2\2\2\u015a\u015b\7v\2\2\u015b")
        buf.write("\u015c\7t\2\2\u015c\u015d\7{\2\2\u015d(\3\2\2\2\u015e")
        buf.write("\u015f\7h\2\2\u015f\u0160\7k\2\2\u0160\u0161\7p\2\2\u0161")
        buf.write("\u0162\7c\2\2\u0162\u0163\7n\2\2\u0163\u0164\7n\2\2\u0164")
        buf.write("\u0165\7{\2\2\u0165*\3\2\2\2\u0166\u0167\7y\2\2\u0167")
        buf.write("\u0168\7k\2\2\u0168\u0169\7v\2\2\u0169\u016a\7j\2\2\u016a")
        buf.write(",\3\2\2\2\u016b\u016c\7g\2\2\u016c\u016d\7z\2\2\u016d")
        buf.write("\u016e\7e\2\2\u016e\u016f\7g\2\2\u016f\u0170\7r\2\2\u0170")
        buf.write("\u0171\7v\2\2\u0171.\3\2\2\2\u0172\u0173\7n\2\2\u0173")
        buf.write("\u0174\7c\2\2\u0174\u0175\7o\2\2\u0175\u0176\7d\2\2\u0176")
        buf.write("\u0177\7f\2\2\u0177\u0178\7c\2\2\u0178\60\3\2\2\2\u0179")
        buf.write("\u017a\7q\2\2\u017a\u017b\7t\2\2\u017b\62\3\2\2\2\u017c")
        buf.write("\u017d\7c\2\2\u017d\u017e\7p\2\2\u017e\u017f\7f\2\2\u017f")
        buf.write("\64\3\2\2\2\u0180\u0181\7p\2\2\u0181\u0182\7q\2\2\u0182")
        buf.write("\u0183\7v\2\2\u0183\66\3\2\2\2\u0184\u0185\7k\2\2\u0185")
        buf.write("\u0186\7u\2\2\u01868\3\2\2\2\u0187\u0188\7p\2\2\u0188")
        buf.write("\u0189\7q\2\2\u0189\u018a\7p\2\2\u018a\u018b\7g\2\2\u018b")
        buf.write(":\3\2\2\2\u018c\u018d\7v\2\2\u018d\u018e\7t\2\2\u018e")
        buf.write("\u018f\7w\2\2\u018f\u0190\7g\2\2\u0190<\3\2\2\2\u0191")
        buf.write("\u0192\7h\2\2\u0192\u0193\7c\2\2\u0193\u0194\7n\2\2\u0194")
        buf.write("\u0195\7u\2\2\u0195\u0196\7g\2\2\u0196>\3\2\2\2\u0197")
        buf.write("\u0198\7e\2\2\u0198\u0199\7n\2\2\u0199\u019a\7c\2\2\u019a")
        buf.write("\u019b\7u\2\2\u019b\u019c\7u\2\2\u019c@\3\2\2\2\u019d")
        buf.write("\u019e\7{\2\2\u019e\u019f\7k\2\2\u019f\u01a0\7g\2\2\u01a0")
        buf.write("\u01a1\7n\2\2\u01a1\u01a2\7f\2\2\u01a2B\3\2\2\2\u01a3")
        buf.write("\u01a4\7f\2\2\u01a4\u01a5\7g\2\2\u01a5\u01a6\7n\2\2\u01a6")
        buf.write("D\3\2\2\2\u01a7\u01a8\7r\2\2\u01a8\u01a9\7c\2\2\u01a9")
        buf.write("\u01aa\7u\2\2\u01aa\u01ab\7u\2\2\u01abF\3\2\2\2\u01ac")
        buf.write("\u01ad\7e\2\2\u01ad\u01ae\7q\2\2\u01ae\u01af\7p\2\2\u01af")
        buf.write("\u01b0\7v\2\2\u01b0\u01b1\7k\2\2\u01b1\u01b2\7p\2\2\u01b2")
        buf.write("\u01b3\7w\2\2\u01b3\u01b4\7g\2\2\u01b4H\3\2\2\2\u01b5")
        buf.write("\u01b6\7d\2\2\u01b6\u01b7\7t\2\2\u01b7\u01b8\7g\2\2\u01b8")
        buf.write("\u01b9\7c\2\2\u01b9\u01ba\7m\2\2\u01baJ\3\2\2\2\u01bb")
        buf.write("\u01bc\7c\2\2\u01bc\u01bd\7u\2\2\u01bd\u01be\7{\2\2\u01be")
        buf.write("\u01bf\7p\2\2\u01bf\u01c0\7e\2\2\u01c0L\3\2\2\2\u01c1")
        buf.write("\u01c2\7c\2\2\u01c2\u01c3\7y\2\2\u01c3\u01c4\7c\2\2\u01c4")
        buf.write("\u01c5\7k\2\2\u01c5\u01c6\7v\2\2\u01c6N\3\2\2\2\u01c7")
        buf.write("\u01c8\6(\2\2\u01c8\u01d4\5\u00f1y\2\u01c9\u01cb\7\17")
        buf.write("\2\2\u01ca\u01c9\3\2\2\2\u01ca\u01cb\3\2\2\2\u01cb\u01cc")
        buf.write("\3\2\2\2\u01cc\u01cf\7\f\2\2\u01cd\u01cf\4\16\17\2\u01ce")
        buf.write("\u01ca\3\2\2\2\u01ce\u01cd\3\2\2\2\u01cf\u01d1\3\2\2\2")
        buf.write("\u01d0\u01d2\5\u00f1y\2\u01d1\u01d0\3\2\2\2\u01d1\u01d2")
        buf.write("\3\2\2\2\u01d2\u01d4\3\2\2\2\u01d3\u01c7\3\2\2\2\u01d3")
        buf.write("\u01ce\3\2\2\2\u01d4\u01d5\3\2\2\2\u01d5\u01d6\b(\2\2")
        buf.write("\u01d6P\3\2\2\2\u01d7\u01db\5\u00f7|\2\u01d8\u01da\5\u00f9")
        buf.write("}\2\u01d9\u01d8\3\2\2\2\u01da\u01dd\3\2\2\2\u01db\u01d9")
        buf.write("\3\2\2\2\u01db\u01dc\3\2\2\2\u01dcR\3\2\2\2\u01dd\u01db")
        buf.write("\3\2\2\2\u01de\u01e4\t\2\2\2\u01df\u01e0\t\3\2\2\u01e0")
        buf.write("\u01e4\t\4\2\2\u01e1\u01e2\t\4\2\2\u01e2\u01e4\t\3\2\2")
        buf.write("\u01e3\u01de\3\2\2\2\u01e3\u01df\3\2\2\2\u01e3\u01e1\3")
        buf.write("\2\2\2\u01e3\u01e4\3\2\2\2\u01e4\u01e7\3\2\2\2\u01e5\u01e8")
        buf.write("\5\u00c5c\2\u01e6\u01e8\5\u00c7d\2\u01e7\u01e5\3\2\2\2")
        buf.write("\u01e7\u01e6\3\2\2\2\u01e8T\3\2\2\2\u01e9\u01ef\t\5\2")
        buf.write("\2\u01ea\u01eb\t\5\2\2\u01eb\u01ef\t\4\2\2\u01ec\u01ed")
        buf.write("\t\4\2\2\u01ed\u01ef\t\5\2\2\u01ee\u01e9\3\2\2\2\u01ee")
        buf.write("\u01ea\3\2\2\2\u01ee\u01ec\3\2\2\2\u01ef\u01f2\3\2\2\2")
        buf.write("\u01f0\u01f3\5\u00e3r\2\u01f1\u01f3\5\u00e5s\2\u01f2\u01f0")
        buf.write("\3\2\2\2\u01f2\u01f1\3\2\2\2\u01f3V\3\2\2\2\u01f4\u01f8")
        buf.write("\5\u00cfh\2\u01f5\u01f7\5\u00d1i\2\u01f6\u01f5\3\2\2\2")
        buf.write("\u01f7\u01fa\3\2\2\2\u01f8\u01f6\3\2\2\2\u01f8\u01f9\3")
        buf.write("\2\2\2\u01f9\u0201\3\2\2\2\u01fa\u01f8\3\2\2\2\u01fb\u01fd")
        buf.write("\7\62\2\2\u01fc\u01fb\3\2\2\2\u01fd\u01fe\3\2\2\2\u01fe")
        buf.write("\u01fc\3\2\2\2\u01fe\u01ff\3\2\2\2\u01ff\u0201\3\2\2\2")
        buf.write("\u0200\u01f4\3\2\2\2\u0200\u01fc\3\2\2\2\u0201X\3\2\2")
        buf.write("\2\u0202\u0203\7\62\2\2\u0203\u0205\t\6\2\2\u0204\u0206")
        buf.write("\5\u00d3j\2\u0205\u0204\3\2\2\2\u0206\u0207\3\2\2\2\u0207")
        buf.write("\u0205\3\2\2\2\u0207\u0208\3\2\2\2\u0208Z\3\2\2\2\u0209")
        buf.write("\u020a\7\62\2\2\u020a\u020c\t\7\2\2\u020b\u020d\5\u00d5")
        buf.write("k\2\u020c\u020b\3\2\2\2\u020d\u020e\3\2\2\2\u020e\u020c")
        buf.write("\3\2\2\2\u020e\u020f\3\2\2\2\u020f\\\3\2\2\2\u0210\u0211")
        buf.write("\7\62\2\2\u0211\u0213\t\5\2\2\u0212\u0214\5\u00d7l\2\u0213")
        buf.write("\u0212\3\2\2\2\u0214\u0215\3\2\2\2\u0215\u0213\3\2\2\2")
        buf.write("\u0215\u0216\3\2\2\2\u0216^\3\2\2\2\u0217\u021a\5\u00d9")
        buf.write("m\2\u0218\u021a\5\u00dbn\2\u0219\u0217\3\2\2\2\u0219\u0218")
        buf.write("\3\2\2\2\u021a`\3\2\2\2\u021b\u021e\5_\60\2\u021c\u021e")
        buf.write("\5\u00ddo\2\u021d\u021b\3\2\2\2\u021d\u021c\3\2\2\2\u021e")
        buf.write("\u021f\3\2\2\2\u021f\u0220\t\b\2\2\u0220b\3\2\2\2\u0221")
        buf.write("\u0222\7\60\2\2\u0222d\3\2\2\2\u0223\u0224\7\60\2\2\u0224")
        buf.write("\u0225\7\60\2\2\u0225\u0226\7\60\2\2\u0226f\3\2\2\2\u0227")
        buf.write("\u0228\7,\2\2\u0228h\3\2\2\2\u0229\u022a\7*\2\2\u022a")
        buf.write("\u022b\b\65\3\2\u022bj\3\2\2\2\u022c\u022d\7+\2\2\u022d")
        buf.write("\u022e\b\66\4\2\u022el\3\2\2\2\u022f\u0230\7.\2\2\u0230")
        buf.write("n\3\2\2\2\u0231\u0232\7<\2\2\u0232p\3\2\2\2\u0233\u0234")
        buf.write("\7=\2\2\u0234r\3\2\2\2\u0235\u0236\7,\2\2\u0236\u0237")
        buf.write("\7,\2\2\u0237t\3\2\2\2\u0238\u0239\7?\2\2\u0239v\3\2\2")
        buf.write("\2\u023a\u023b\7]\2\2\u023b\u023c\b<\5\2\u023cx\3\2\2")
        buf.write("\2\u023d\u023e\7_\2\2\u023e\u023f\b=\6\2\u023fz\3\2\2")
        buf.write("\2\u0240\u0241\7~\2\2\u0241|\3\2\2\2\u0242\u0243\7`\2")
        buf.write("\2\u0243~\3\2\2\2\u0244\u0245\7(\2\2\u0245\u0080\3\2\2")
        buf.write("\2\u0246\u0247\7>\2\2\u0247\u0248\7>\2\2\u0248\u0082\3")
        buf.write("\2\2\2\u0249\u024a\7@\2\2\u024a\u024b\7@\2\2\u024b\u0084")
        buf.write("\3\2\2\2\u024c\u024d\7-\2\2\u024d\u0086\3\2\2\2\u024e")
        buf.write("\u024f\7/\2\2\u024f\u0088\3\2\2\2\u0250\u0251\7\61\2\2")
        buf.write("\u0251\u008a\3\2\2\2\u0252\u0253\7\'\2\2\u0253\u008c\3")
        buf.write("\2\2\2\u0254\u0255\7\61\2\2\u0255\u0256\7\61\2\2\u0256")
        buf.write("\u008e\3\2\2\2\u0257\u0258\7\u0080\2\2\u0258\u0090\3\2")
        buf.write("\2\2\u0259\u025a\7}\2\2\u025a\u025b\bI\7\2\u025b\u0092")
        buf.write("\3\2\2\2\u025c\u025d\7\177\2\2\u025d\u025e\bJ\b\2\u025e")
        buf.write("\u0094\3\2\2\2\u025f\u0260\7>\2\2\u0260\u0096\3\2\2\2")
        buf.write("\u0261\u0262\7@\2\2\u0262\u0098\3\2\2\2\u0263\u0264\7")
        buf.write("?\2\2\u0264\u0265\7?\2\2\u0265\u009a\3\2\2\2\u0266\u0267")
        buf.write("\7@\2\2\u0267\u0268\7?\2\2\u0268\u009c\3\2\2\2\u0269\u026a")
        buf.write("\7>\2\2\u026a\u026b\7?\2\2\u026b\u009e\3\2\2\2\u026c\u026d")
        buf.write("\7>\2\2\u026d\u026e\7@\2\2\u026e\u00a0\3\2\2\2\u026f\u0270")
        buf.write("\7#\2\2\u0270\u0271\7?\2\2\u0271\u00a2\3\2\2\2\u0272\u0273")
        buf.write("\7B\2\2\u0273\u00a4\3\2\2\2\u0274\u0275\7/\2\2\u0275\u0276")
        buf.write("\7@\2\2\u0276\u00a6\3\2\2\2\u0277\u0278\7-\2\2\u0278\u0279")
        buf.write("\7?\2\2\u0279\u00a8\3\2\2\2\u027a\u027b\7/\2\2\u027b\u027c")
        buf.write("\7?\2\2\u027c\u00aa\3\2\2\2\u027d\u027e\7,\2\2\u027e\u027f")
        buf.write("\7?\2\2\u027f\u00ac\3\2\2\2\u0280\u0281\7B\2\2\u0281\u0282")
        buf.write("\7?\2\2\u0282\u00ae\3\2\2\2\u0283\u0284\7\61\2\2\u0284")
        buf.write("\u0285\7?\2\2\u0285\u00b0\3\2\2\2\u0286\u0287\7\'\2\2")
        buf.write("\u0287\u0288\7?\2\2\u0288\u00b2\3\2\2\2\u0289\u028a\7")
        buf.write("(\2\2\u028a\u028b\7?\2\2\u028b\u00b4\3\2\2\2\u028c\u028d")
        buf.write("\7~\2\2\u028d\u028e\7?\2\2\u028e\u00b6\3\2\2\2\u028f\u0290")
        buf.write("\7`\2\2\u0290\u0291\7?\2\2\u0291\u00b8\3\2\2\2\u0292\u0293")
        buf.write("\7>\2\2\u0293\u0294\7>\2\2\u0294\u0295\7?\2\2\u0295\u00ba")
        buf.write("\3\2\2\2\u0296\u0297\7@\2\2\u0297\u0298\7@\2\2\u0298\u0299")
        buf.write("\7?\2\2\u0299\u00bc\3\2\2\2\u029a\u029b\7,\2\2\u029b\u029c")
        buf.write("\7,\2\2\u029c\u029d\7?\2\2\u029d\u00be\3\2\2\2\u029e\u029f")
        buf.write("\7\61\2\2\u029f\u02a0\7\61\2\2\u02a0\u02a1\7?\2\2\u02a1")
        buf.write("\u00c0\3\2\2\2\u02a2\u02a6\5\u00f1y\2\u02a3\u02a6\5\u00f3")
        buf.write("z\2\u02a4\u02a6\5\u00f5{\2\u02a5\u02a2\3\2\2\2\u02a5\u02a3")
        buf.write("\3\2\2\2\u02a5\u02a4\3\2\2\2\u02a6\u02a7\3\2\2\2\u02a7")
        buf.write("\u02a8\ba\t\2\u02a8\u00c2\3\2\2\2\u02a9\u02aa\13\2\2\2")
        buf.write("\u02aa\u00c4\3\2\2\2\u02ab\u02b0\7)\2\2\u02ac\u02af\5")
        buf.write("\u00cdg\2\u02ad\u02af\n\t\2\2\u02ae\u02ac\3\2\2\2\u02ae")
        buf.write("\u02ad\3\2\2\2\u02af\u02b2\3\2\2\2\u02b0\u02ae\3\2\2\2")
        buf.write("\u02b0\u02b1\3\2\2\2\u02b1\u02b3\3\2\2\2\u02b2\u02b0\3")
        buf.write("\2\2\2\u02b3\u02be\7)\2\2\u02b4\u02b9\7$\2\2\u02b5\u02b8")
        buf.write("\5\u00cdg\2\u02b6\u02b8\n\n\2\2\u02b7\u02b5\3\2\2\2\u02b7")
        buf.write("\u02b6\3\2\2\2\u02b8\u02bb\3\2\2\2\u02b9\u02b7\3\2\2\2")
        buf.write("\u02b9\u02ba\3\2\2\2\u02ba\u02bc\3\2\2\2\u02bb\u02b9\3")
        buf.write("\2\2\2\u02bc\u02be\7$\2\2\u02bd\u02ab\3\2\2\2\u02bd\u02b4")
        buf.write("\3\2\2\2\u02be\u00c6\3\2\2\2\u02bf\u02c0\7)\2\2\u02c0")
        buf.write("\u02c1\7)\2\2\u02c1\u02c2\7)\2\2\u02c2\u02c6\3\2\2\2\u02c3")
        buf.write("\u02c5\5\u00c9e\2\u02c4\u02c3\3\2\2\2\u02c5\u02c8\3\2")
        buf.write("\2\2\u02c6\u02c7\3\2\2\2\u02c6\u02c4\3\2\2\2\u02c7\u02c9")
        buf.write("\3\2\2\2\u02c8\u02c6\3\2\2\2\u02c9\u02ca\7)\2\2\u02ca")
        buf.write("\u02cb\7)\2\2\u02cb\u02da\7)\2\2\u02cc\u02cd\7$\2\2\u02cd")
        buf.write("\u02ce\7$\2\2\u02ce\u02cf\7$\2\2\u02cf\u02d3\3\2\2\2\u02d0")
        buf.write("\u02d2\5\u00c9e\2\u02d1\u02d0\3\2\2\2\u02d2\u02d5\3\2")
        buf.write("\2\2\u02d3\u02d4\3\2\2\2\u02d3\u02d1\3\2\2\2\u02d4\u02d6")
        buf.write("\3\2\2\2\u02d5\u02d3\3\2\2\2\u02d6\u02d7\7$\2\2\u02d7")
        buf.write("\u02d8\7$\2\2\u02d8\u02da\7$\2\2\u02d9\u02bf\3\2\2\2\u02d9")
        buf.write("\u02cc\3\2\2\2\u02da\u00c8\3\2\2\2\u02db\u02de\5\u00cb")
        buf.write("f\2\u02dc\u02de\5\u00cdg\2\u02dd\u02db\3\2\2\2\u02dd\u02dc")
        buf.write("\3\2\2\2\u02de\u00ca\3\2\2\2\u02df\u02e0\n\13\2\2\u02e0")
        buf.write("\u00cc\3\2\2\2\u02e1\u02e2\7^\2\2\u02e2\u02e6\13\2\2\2")
        buf.write("\u02e3\u02e4\7^\2\2\u02e4\u02e6\5O(\2\u02e5\u02e1\3\2")
        buf.write("\2\2\u02e5\u02e3\3\2\2\2\u02e6\u00ce\3\2\2\2\u02e7\u02e8")
        buf.write("\t\f\2\2\u02e8\u00d0\3\2\2\2\u02e9\u02ea\t\r\2\2\u02ea")
        buf.write("\u00d2\3\2\2\2\u02eb\u02ec\t\16\2\2\u02ec\u00d4\3\2\2")
        buf.write("\2\u02ed\u02ee\t\17\2\2\u02ee\u00d6\3\2\2\2\u02ef\u02f0")
        buf.write("\t\20\2\2\u02f0\u00d8\3\2\2\2\u02f1\u02f3\5\u00ddo\2\u02f2")
        buf.write("\u02f1\3\2\2\2\u02f2\u02f3\3\2\2\2\u02f3\u02f4\3\2\2\2")
        buf.write("\u02f4\u02f9\5\u00dfp\2\u02f5\u02f6\5\u00ddo\2\u02f6\u02f7")
        buf.write("\7\60\2\2\u02f7\u02f9\3\2\2\2\u02f8\u02f2\3\2\2\2\u02f8")
        buf.write("\u02f5\3\2\2\2\u02f9\u00da\3\2\2\2\u02fa\u02fd\5\u00dd")
        buf.write("o\2\u02fb\u02fd\5\u00d9m\2\u02fc\u02fa\3\2\2\2\u02fc\u02fb")
        buf.write("\3\2\2\2\u02fd\u02fe\3\2\2\2\u02fe\u02ff\5\u00e1q\2\u02ff")
        buf.write("\u00dc\3\2\2\2\u0300\u0302\5\u00d1i\2\u0301\u0300\3\2")
        buf.write("\2\2\u0302\u0303\3\2\2\2\u0303\u0301\3\2\2\2\u0303\u0304")
        buf.write("\3\2\2\2\u0304\u00de\3\2\2\2\u0305\u0307\7\60\2\2\u0306")
        buf.write("\u0308\5\u00d1i\2\u0307\u0306\3\2\2\2\u0308\u0309\3\2")
        buf.write("\2\2\u0309\u0307\3\2\2\2\u0309\u030a\3\2\2\2\u030a\u00e0")
        buf.write("\3\2\2\2\u030b\u030d\t\21\2\2\u030c\u030e\t\22\2\2\u030d")
        buf.write("\u030c\3\2\2\2\u030d\u030e\3\2\2\2\u030e\u0310\3\2\2\2")
        buf.write("\u030f\u0311\5\u00d1i\2\u0310\u030f\3\2\2\2\u0311\u0312")
        buf.write("\3\2\2\2\u0312\u0310\3\2\2\2\u0312\u0313\3\2\2\2\u0313")
        buf.write("\u00e2\3\2\2\2\u0314\u0319\7)\2\2\u0315\u0318\5\u00e9")
        buf.write("u\2\u0316\u0318\5\u00efx\2\u0317\u0315\3\2\2\2\u0317\u0316")
        buf.write("\3\2\2\2\u0318\u031b\3\2\2\2\u0319\u0317\3\2\2\2\u0319")
        buf.write("\u031a\3\2\2\2\u031a\u031c\3\2\2\2\u031b\u0319\3\2\2\2")
        buf.write("\u031c\u0327\7)\2\2\u031d\u0322\7$\2\2\u031e\u0321\5\u00eb")
        buf.write("v\2\u031f\u0321\5\u00efx\2\u0320\u031e\3\2\2\2\u0320\u031f")
        buf.write("\3\2\2\2\u0321\u0324\3\2\2\2\u0322\u0320\3\2\2\2\u0322")
        buf.write("\u0323\3\2\2\2\u0323\u0325\3\2\2\2\u0324\u0322\3\2\2\2")
        buf.write("\u0325\u0327\7$\2\2\u0326\u0314\3\2\2\2\u0326\u031d\3")
        buf.write("\2\2\2\u0327\u00e4\3\2\2\2\u0328\u0329\7)\2\2\u0329\u032a")
        buf.write("\7)\2\2\u032a\u032b\7)\2\2\u032b\u032f\3\2\2\2\u032c\u032e")
        buf.write("\5\u00e7t\2\u032d\u032c\3\2\2\2\u032e\u0331\3\2\2\2\u032f")
        buf.write("\u0330\3\2\2\2\u032f\u032d\3\2\2\2\u0330\u0332\3\2\2\2")
        buf.write("\u0331\u032f\3\2\2\2\u0332\u0333\7)\2\2\u0333\u0334\7")
        buf.write(")\2\2\u0334\u0343\7)\2\2\u0335\u0336\7$\2\2\u0336\u0337")
        buf.write("\7$\2\2\u0337\u0338\7$\2\2\u0338\u033c\3\2\2\2\u0339\u033b")
        buf.write("\5\u00e7t\2\u033a\u0339\3\2\2\2\u033b\u033e\3\2\2\2\u033c")
        buf.write("\u033d\3\2\2\2\u033c\u033a\3\2\2\2\u033d\u033f\3\2\2\2")
        buf.write("\u033e\u033c\3\2\2\2\u033f\u0340\7$\2\2\u0340\u0341\7")
        buf.write("$\2\2\u0341\u0343\7$\2\2\u0342\u0328\3\2\2\2\u0342\u0335")
        buf.write("\3\2\2\2\u0343\u00e6\3\2\2\2\u0344\u0347\5\u00edw\2\u0345")
        buf.write("\u0347\5\u00efx\2\u0346\u0344\3\2\2\2\u0346\u0345\3\2")
        buf.write("\2\2\u0347\u00e8\3\2\2\2\u0348\u034a\t\23\2\2\u0349\u0348")
        buf.write("\3\2\2\2\u034a\u00ea\3\2\2\2\u034b\u034d\t\24\2\2\u034c")
        buf.write("\u034b\3\2\2\2\u034d\u00ec\3\2\2\2\u034e\u0350\t\25\2")
        buf.write("\2\u034f\u034e\3\2\2\2\u0350\u00ee\3\2\2\2\u0351\u0352")
        buf.write("\7^\2\2\u0352\u0353\t\26\2\2\u0353\u00f0\3\2\2\2\u0354")
        buf.write("\u0356\t\27\2\2\u0355\u0354\3\2\2\2\u0356\u0357\3\2\2")
        buf.write("\2\u0357\u0355\3\2\2\2\u0357\u0358\3\2\2\2\u0358\u00f2")
        buf.write("\3\2\2\2\u0359\u035d\7%\2\2\u035a\u035c\n\30\2\2\u035b")
        buf.write("\u035a\3\2\2\2\u035c\u035f\3\2\2\2\u035d\u035b\3\2\2\2")
        buf.write("\u035d\u035e\3\2\2\2\u035e\u00f4\3\2\2\2\u035f\u035d\3")
        buf.write("\2\2\2\u0360\u0362\7^\2\2\u0361\u0363\5\u00f1y\2\u0362")
        buf.write("\u0361\3\2\2\2\u0362\u0363\3\2\2\2\u0363\u0369\3\2\2\2")
        buf.write("\u0364\u0366\7\17\2\2\u0365\u0364\3\2\2\2\u0365\u0366")
        buf.write("\3\2\2\2\u0366\u0367\3\2\2\2\u0367\u036a\7\f\2\2\u0368")
        buf.write("\u036a\4\16\17\2\u0369\u0365\3\2\2\2\u0369\u0368\3\2\2")
        buf.write("\2\u036a\u00f6\3\2\2\2\u036b\u036d\t\31\2\2\u036c\u036b")
        buf.write("\3\2\2\2\u036d\u00f8\3\2\2\2\u036e\u0371\5\u00f7|\2\u036f")
        buf.write("\u0371\t\32\2\2\u0370\u036e\3\2\2\2\u0370\u036f\3\2\2")
        buf.write("\2\u0371\u00fa\3\2\2\2;\2\u0101\u0107\u01ca\u01ce\u01d1")
        buf.write("\u01d3\u01db\u01e3\u01e7\u01ee\u01f2\u01f8\u01fe\u0200")
        buf.write("\u0207\u020e\u0215\u0219\u021d\u02a5\u02ae\u02b0\u02b7")
        buf.write("\u02b9\u02bd\u02c6\u02d3\u02d9\u02dd\u02e5\u02f2\u02f8")
        buf.write("\u02fc\u0303\u0309\u030d\u0312\u0317\u0319\u0320\u0322")
        buf.write("\u0326\u032f\u033c\u0342\u0346\u0349\u034c\u034f\u0357")
        buf.write("\u035d\u0362\u0365\u0369\u036c\u0370\n\3(\2\3\65\3\3\66")
        buf.write("\4\3<\5\3=\6\3I\7\3J\b\b\2\2")
        return buf.getvalue()


class DrakeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    STRING = 2
    INTEGER = 3
    DEF = 4
    RETURN = 5
    RAISE = 6
    FROM = 7
    IMPORT = 8
    AS = 9
    GLOBAL = 10
    NONLOCAL = 11
    ASSERT = 12
    IF = 13
    ELIF = 14
    ELSE = 15
    WHILE = 16
    FOR = 17
    IN = 18
    TRY = 19
    FINALLY = 20
    WITH = 21
    EXCEPT = 22
    LAMBDA = 23
    OR = 24
    AND = 25
    NOT = 26
    IS = 27
    NONE = 28
    TRUE = 29
    FALSE = 30
    CLASS = 31
    YIELD = 32
    DEL = 33
    PASS = 34
    CONTINUE = 35
    BREAK = 36
    ASYNC = 37
    AWAIT = 38
    NEWLINE = 39
    NAME = 40
    STRING_LITERAL = 41
    BYTES_LITERAL = 42
    DECIMAL_INTEGER = 43
    OCT_INTEGER = 44
    HEX_INTEGER = 45
    BIN_INTEGER = 46
    FLOAT_NUMBER = 47
    IMAG_NUMBER = 48
    DOT = 49
    ELLIPSIS = 50
    STAR = 51
    OPEN_PAREN = 52
    CLOSE_PAREN = 53
    COMMA = 54
    COLON = 55
    SEMI_COLON = 56
    POWER = 57
    ASSIGN = 58
    OPEN_BRACK = 59
    CLOSE_BRACK = 60
    OR_OP = 61
    XOR = 62
    AND_OP = 63
    LEFT_SHIFT = 64
    RIGHT_SHIFT = 65
    ADD = 66
    MINUS = 67
    DIV = 68
    MOD = 69
    IDIV = 70
    NOT_OP = 71
    OPEN_BRACE = 72
    CLOSE_BRACE = 73
    LESS_THAN = 74
    GREATER_THAN = 75
    EQUALS = 76
    GT_EQ = 77
    LT_EQ = 78
    NOT_EQ_1 = 79
    NOT_EQ_2 = 80
    AT = 81
    ARROW = 82
    ADD_ASSIGN = 83
    SUB_ASSIGN = 84
    MULT_ASSIGN = 85
    AT_ASSIGN = 86
    DIV_ASSIGN = 87
    MOD_ASSIGN = 88
    AND_ASSIGN = 89
    OR_ASSIGN = 90
    XOR_ASSIGN = 91
    LEFT_SHIFT_ASSIGN = 92
    RIGHT_SHIFT_ASSIGN = 93
    POWER_ASSIGN = 94
    IDIV_ASSIGN = 95
    SKIP_ = 96
    UNKNOWN_CHAR = 97

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'isa'", "'def'", "'return'", "'raise'", "'from'", "'import'", 
            "'as'", "'global'", "'nonlocal'", "'assert'", "'if'", "'elif'", 
            "'else'", "'while'", "'for'", "'in'", "'try'", "'finally'", 
            "'with'", "'except'", "'lambda'", "'or'", "'and'", "'not'", 
            "'is'", "'none'", "'true'", "'false'", "'class'", "'yield'", 
            "'del'", "'pass'", "'continue'", "'break'", "'async'", "'await'", 
            "'.'", "'...'", "'*'", "'('", "')'", "','", "':'", "';'", "'**'", 
            "'='", "'['", "']'", "'|'", "'^'", "'&'", "'<<'", "'>>'", "'+'", 
            "'-'", "'/'", "'%'", "'//'", "'~'", "'{'", "'}'", "'<'", "'>'", 
            "'=='", "'>='", "'<='", "'<>'", "'!='", "'@'", "'->'", "'+='", 
            "'-='", "'*='", "'@='", "'/='", "'%='", "'&='", "'|='", "'^='", 
            "'<<='", "'>>='", "'**='", "'//='" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "INTEGER", "DEF", "RETURN", "RAISE", "FROM", "IMPORT", 
            "AS", "GLOBAL", "NONLOCAL", "ASSERT", "IF", "ELIF", "ELSE", 
            "WHILE", "FOR", "IN", "TRY", "FINALLY", "WITH", "EXCEPT", "LAMBDA", 
            "OR", "AND", "NOT", "IS", "NONE", "TRUE", "FALSE", "CLASS", 
            "YIELD", "DEL", "PASS", "CONTINUE", "BREAK", "ASYNC", "AWAIT", 
            "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", 
            "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", 
            "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", "CLOSE_PAREN", 
            "COMMA", "COLON", "SEMI_COLON", "POWER", "ASSIGN", "OPEN_BRACK", 
            "CLOSE_BRACK", "OR_OP", "XOR", "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", 
            "ADD", "MINUS", "DIV", "MOD", "IDIV", "NOT_OP", "OPEN_BRACE", 
            "CLOSE_BRACE", "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", 
            "LT_EQ", "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", 
            "SUB_ASSIGN", "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
            "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
            "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
            "UNKNOWN_CHAR" ]

    ruleNames = [ "T__0", "STRING", "INTEGER", "DEF", "RETURN", "RAISE", 
                  "FROM", "IMPORT", "AS", "GLOBAL", "NONLOCAL", "ASSERT", 
                  "IF", "ELIF", "ELSE", "WHILE", "FOR", "IN", "TRY", "FINALLY", 
                  "WITH", "EXCEPT", "LAMBDA", "OR", "AND", "NOT", "IS", 
                  "NONE", "TRUE", "FALSE", "CLASS", "YIELD", "DEL", "PASS", 
                  "CONTINUE", "BREAK", "ASYNC", "AWAIT", "NEWLINE", "NAME", 
                  "STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", 
                  "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", 
                  "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
                  "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", 
                  "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", 
                  "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", 
                  "DIV", "MOD", "IDIV", "NOT_OP", "OPEN_BRACE", "CLOSE_BRACE", 
                  "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", "LT_EQ", 
                  "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", "SUB_ASSIGN", 
                  "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
                  "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
                  "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
                  "UNKNOWN_CHAR", "SHORT_STRING", "LONG_STRING", "LONG_STRING_ITEM", 
                  "LONG_STRING_CHAR", "STRING_ESCAPE_SEQ", "NON_ZERO_DIGIT", 
                  "DIGIT", "OCT_DIGIT", "HEX_DIGIT", "BIN_DIGIT", "POINT_FLOAT", 
                  "EXPONENT_FLOAT", "INT_PART", "FRACTION", "EXPONENT", 
                  "SHORT_BYTES", "LONG_BYTES", "LONG_BYTES_ITEM", "SHORT_BYTES_CHAR_NO_SINGLE_QUOTE", 
                  "SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE", "LONG_BYTES_CHAR", 
                  "BYTES_ESCAPE_SEQ", "SPACES", "COMMENT", "LINE_JOINING", 
                  "ID_START", "ID_CONTINUE" ]

    grammarFileName = "Drake.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens

    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents

    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value

    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken

    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value

    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None

    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)

    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)

            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()

            self.emitToken(self.commonToken(LanguageParser.EOF, "<EOF>"))
        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)

    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent

    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)

    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count

    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[38] = self.NEWLINE_action 
            actions[51] = self.OPEN_PAREN_action 
            actions[52] = self.CLOSE_PAREN_action 
            actions[58] = self.OPEN_BRACK_action 
            actions[59] = self.CLOSE_BRACK_action 
            actions[71] = self.OPEN_BRACE_action 
            actions[72] = self.CLOSE_BRACE_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))

    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            tempt = Lexer.text.fget(self)
            newLine = re.sub("[^\r\n\f]+", "", tempt)
            spaces = re.sub("[\r\n\f]+", "", tempt)
            la_char = ""
            try:
                la = self._input.LA(1)
                la_char = chr(la)       # Python does not compare char to ints directly
            except ValueError:          # End of file
                pass

            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False

            if self.opened > 0 or nextnext_eof is False and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, newLine, indent=indent))      # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def OPEN_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:
            self.opened += 1
     

    def CLOSE_BRACE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            self.opened -= 1
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[38] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


