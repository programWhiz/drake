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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2e")
        buf.write("\u037e\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
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
        buf.write("y\ty\4z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\3\2\3\2")
        buf.write("\3\2\3\2\3\3\3\3\5\3\u0106\n\3\3\4\3\4\3\4\3\4\5\4\u010c")
        buf.write("\n\4\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\3")
        buf.write("\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13")
        buf.write("\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3")
        buf.write("\r\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20")
        buf.write("\3\20\3\20\3\20\3\20\3\21\3\21\3\21\3\21\3\21\3\21\3\22")
        buf.write("\3\22\3\22\3\23\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\27\3\27\3\27")
        buf.write("\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30\3\30\3\31")
        buf.write("\3\31\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32")
        buf.write("\3\32\3\32\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\35\3\35")
        buf.write("\3\35\3\35\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3 ")
        buf.write("\3 \3 \3 \3 \3!\3!\3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3\"")
        buf.write("\3#\3#\3#\3#\3#\3#\3$\3$\3$\3$\3%\3%\3%\3%\3%\3&\3&\3")
        buf.write("&\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3(\3")
        buf.write("(\3(\3(\3)\3)\3)\3)\3)\3)\3*\3*\3*\5*\u01d7\n*\3*\3*\5")
        buf.write("*\u01db\n*\3*\5*\u01de\n*\5*\u01e0\n*\3*\3*\3+\3+\7+\u01e6")
        buf.write("\n+\f+\16+\u01e9\13+\3,\3,\3,\3,\3,\5,\u01f0\n,\3,\3,")
        buf.write("\5,\u01f4\n,\3-\3-\3-\3-\3-\5-\u01fb\n-\3-\3-\5-\u01ff")
        buf.write("\n-\3.\3.\7.\u0203\n.\f.\16.\u0206\13.\3.\6.\u0209\n.")
        buf.write("\r.\16.\u020a\5.\u020d\n.\3/\3/\3/\6/\u0212\n/\r/\16/")
        buf.write("\u0213\3\60\3\60\3\60\6\60\u0219\n\60\r\60\16\60\u021a")
        buf.write("\3\61\3\61\3\61\6\61\u0220\n\61\r\61\16\61\u0221\3\62")
        buf.write("\3\62\5\62\u0226\n\62\3\63\3\63\5\63\u022a\n\63\3\63\3")
        buf.write("\63\3\64\3\64\3\65\3\65\3\65\3\65\3\66\3\66\3\67\3\67")
        buf.write("\3\67\38\38\38\39\39\3:\3:\3;\3;\3<\3<\3<\3=\3=\3>\3>")
        buf.write("\3>\3?\3?\3?\3@\3@\3A\3A\3B\3B\3C\3C\3C\3D\3D\3D\3E\3")
        buf.write("E\3F\3F\3G\3G\3H\3H\3I\3I\3I\3J\3J\3K\3K\3K\3L\3L\3L\3")
        buf.write("M\3M\3N\3N\3O\3O\3O\3P\3P\3P\3Q\3Q\3Q\3R\3R\3R\3S\3S\3")
        buf.write("S\3T\3T\3U\3U\3U\3V\3V\3V\3W\3W\3W\3X\3X\3X\3Y\3Y\3Y\3")
        buf.write("Z\3Z\3Z\3[\3[\3[\3\\\3\\\3\\\3]\3]\3]\3^\3^\3^\3_\3_\3")
        buf.write("_\3_\3`\3`\3`\3`\3a\3a\3a\3a\3b\3b\3b\3b\3c\3c\3c\5c\u02b2")
        buf.write("\nc\3c\3c\3d\3d\3e\3e\3e\7e\u02bb\ne\fe\16e\u02be\13e")
        buf.write("\3e\3e\3e\3e\7e\u02c4\ne\fe\16e\u02c7\13e\3e\5e\u02ca")
        buf.write("\ne\3f\3f\3f\3f\3f\7f\u02d1\nf\ff\16f\u02d4\13f\3f\3f")
        buf.write("\3f\3f\3f\3f\3f\3f\7f\u02de\nf\ff\16f\u02e1\13f\3f\3f")
        buf.write("\3f\5f\u02e6\nf\3g\3g\5g\u02ea\ng\3h\3h\3i\3i\3i\3i\5")
        buf.write("i\u02f2\ni\3j\3j\3k\3k\3l\3l\3m\3m\3n\3n\3o\5o\u02ff\n")
        buf.write("o\3o\3o\3o\3o\5o\u0305\no\3p\3p\5p\u0309\np\3p\3p\3q\6")
        buf.write("q\u030e\nq\rq\16q\u030f\3r\3r\6r\u0314\nr\rr\16r\u0315")
        buf.write("\3s\3s\5s\u031a\ns\3s\6s\u031d\ns\rs\16s\u031e\3t\3t\3")
        buf.write("t\7t\u0324\nt\ft\16t\u0327\13t\3t\3t\3t\3t\7t\u032d\n")
        buf.write("t\ft\16t\u0330\13t\3t\5t\u0333\nt\3u\3u\3u\3u\3u\7u\u033a")
        buf.write("\nu\fu\16u\u033d\13u\3u\3u\3u\3u\3u\3u\3u\3u\7u\u0347")
        buf.write("\nu\fu\16u\u034a\13u\3u\3u\3u\5u\u034f\nu\3v\3v\5v\u0353")
        buf.write("\nv\3w\5w\u0356\nw\3x\5x\u0359\nx\3y\5y\u035c\ny\3z\3")
        buf.write("z\3z\3{\6{\u0362\n{\r{\16{\u0363\3|\3|\7|\u0368\n|\f|")
        buf.write("\16|\u036b\13|\3}\3}\5}\u036f\n}\3}\5}\u0372\n}\3}\3}")
        buf.write("\5}\u0376\n}\3~\5~\u0379\n~\3\177\3\177\5\177\u037d\n")
        buf.write("\177\6\u02d2\u02df\u033b\u0348\2\u0080\3\3\5\4\7\5\t\6")
        buf.write("\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65")
        buf.write("\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60")
        buf.write("_\61a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081")
        buf.write("B\u0083C\u0085D\u0087E\u0089F\u008bG\u008dH\u008fI\u0091")
        buf.write("J\u0093K\u0095L\u0097M\u0099N\u009bO\u009dP\u009fQ\u00a1")
        buf.write("R\u00a3S\u00a5T\u00a7U\u00a9V\u00abW\u00adX\u00afY\u00b1")
        buf.write("Z\u00b3[\u00b5\\\u00b7]\u00b9^\u00bb_\u00bd`\u00bfa\u00c1")
        buf.write("b\u00c3c\u00c5d\u00c7e\u00c9\2\u00cb\2\u00cd\2\u00cf\2")
        buf.write("\u00d1\2\u00d3\2\u00d5\2\u00d7\2\u00d9\2\u00db\2\u00dd")
        buf.write("\2\u00df\2\u00e1\2\u00e3\2\u00e5\2\u00e7\2\u00e9\2\u00eb")
        buf.write("\2\u00ed\2\u00ef\2\u00f1\2\u00f3\2\u00f5\2\u00f7\2\u00f9")
        buf.write("\2\u00fb\2\u00fd\2\3\2\33\b\2HHTTWWhhttww\4\2HHhh\4\2")
        buf.write("TTtt\4\2DDdd\4\2QQqq\4\2ZZzz\4\2LLll\6\2\f\f\16\17))^")
        buf.write("^\6\2\f\f\16\17$$^^\3\2^^\3\2\63;\3\2\62;\3\2\629\5\2")
        buf.write("\62;CHch\3\2\62\63\4\2GGgg\4\2--//\7\2\2\13\r\16\20(*")
        buf.write("]_\u0081\7\2\2\13\r\16\20#%]_\u0081\4\2\2]_\u0081\3\2")
        buf.write("\2\u0081\4\2\13\13\"\"\4\2\f\f\16\17\u0129\2C\\aac|\u00ac")
        buf.write("\u00ac\u00b7\u00b7\u00bc\u00bc\u00c2\u00d8\u00da\u00f8")
        buf.write("\u00fa\u0243\u0252\u02c3\u02c8\u02d3\u02e2\u02e6\u02f0")
        buf.write("\u02f0\u037c\u037c\u0388\u0388\u038a\u038c\u038e\u038e")
        buf.write("\u0390\u03a3\u03a5\u03d0\u03d2\u03f7\u03f9\u0483\u048c")
        buf.write("\u04d0\u04d2\u04fb\u0502\u0511\u0533\u0558\u055b\u055b")
        buf.write("\u0563\u0589\u05d2\u05ec\u05f2\u05f4\u0623\u063c\u0642")
        buf.write("\u064c\u0670\u0671\u0673\u06d5\u06d7\u06d7\u06e7\u06e8")
        buf.write("\u06f0\u06f1\u06fc\u06fe\u0701\u0701\u0712\u0712\u0714")
        buf.write("\u0731\u074f\u076f\u0782\u07a7\u07b3\u07b3\u0906\u093b")
        buf.write("\u093f\u093f\u0952\u0952\u095a\u0963\u097f\u097f\u0987")
        buf.write("\u098e\u0991\u0992\u0995\u09aa\u09ac\u09b2\u09b4\u09b4")
        buf.write("\u09b8\u09bb\u09bf\u09bf\u09d0\u09d0\u09de\u09df\u09e1")
        buf.write("\u09e3\u09f2\u09f3\u0a07\u0a0c\u0a11\u0a12\u0a15\u0a2a")
        buf.write("\u0a2c\u0a32\u0a34\u0a35\u0a37\u0a38\u0a3a\u0a3b\u0a5b")
        buf.write("\u0a5e\u0a60\u0a60\u0a74\u0a76\u0a87\u0a8f\u0a91\u0a93")
        buf.write("\u0a95\u0aaa\u0aac\u0ab2\u0ab4\u0ab5\u0ab7\u0abb\u0abf")
        buf.write("\u0abf\u0ad2\u0ad2\u0ae2\u0ae3\u0b07\u0b0e\u0b11\u0b12")
        buf.write("\u0b15\u0b2a\u0b2c\u0b32\u0b34\u0b35\u0b37\u0b3b\u0b3f")
        buf.write("\u0b3f\u0b5e\u0b5f\u0b61\u0b63\u0b73\u0b73\u0b85\u0b85")
        buf.write("\u0b87\u0b8c\u0b90\u0b92\u0b94\u0b97\u0b9b\u0b9c\u0b9e")
        buf.write("\u0b9e\u0ba0\u0ba1\u0ba5\u0ba6\u0baa\u0bac\u0bb0\u0bbb")
        buf.write("\u0c07\u0c0e\u0c10\u0c12\u0c14\u0c2a\u0c2c\u0c35\u0c37")
        buf.write("\u0c3b\u0c62\u0c63\u0c87\u0c8e\u0c90\u0c92\u0c94\u0caa")
        buf.write("\u0cac\u0cb5\u0cb7\u0cbb\u0cbf\u0cbf\u0ce0\u0ce0\u0ce2")
        buf.write("\u0ce3\u0d07\u0d0e\u0d10\u0d12\u0d14\u0d2a\u0d2c\u0d3b")
        buf.write("\u0d62\u0d63\u0d87\u0d98\u0d9c\u0db3\u0db5\u0dbd\u0dbf")
        buf.write("\u0dbf\u0dc2\u0dc8\u0e03\u0e32\u0e34\u0e35\u0e42\u0e48")
        buf.write("\u0e83\u0e84\u0e86\u0e86\u0e89\u0e8a\u0e8c\u0e8c\u0e8f")
        buf.write("\u0e8f\u0e96\u0e99\u0e9b\u0ea1\u0ea3\u0ea5\u0ea7\u0ea7")
        buf.write("\u0ea9\u0ea9\u0eac\u0ead\u0eaf\u0eb2\u0eb4\u0eb5\u0ebf")
        buf.write("\u0ebf\u0ec2\u0ec6\u0ec8\u0ec8\u0ede\u0edf\u0f02\u0f02")
        buf.write("\u0f42\u0f49\u0f4b\u0f6c\u0f8a\u0f8d\u1002\u1023\u1025")
        buf.write("\u1029\u102b\u102c\u1052\u1057\u10a2\u10c7\u10d2\u10fc")
        buf.write("\u10fe\u10fe\u1102\u115b\u1161\u11a4\u11aa\u11fb\u1202")
        buf.write("\u124a\u124c\u124f\u1252\u1258\u125a\u125a\u125c\u125f")
        buf.write("\u1262\u128a\u128c\u128f\u1292\u12b2\u12b4\u12b7\u12ba")
        buf.write("\u12c0\u12c2\u12c2\u12c4\u12c7\u12ca\u12d8\u12da\u1312")
        buf.write("\u1314\u1317\u131a\u135c\u1382\u1391\u13a2\u13f6\u1403")
        buf.write("\u166e\u1671\u1678\u1683\u169c\u16a2\u16ec\u16f0\u16f2")
        buf.write("\u1702\u170e\u1710\u1713\u1722\u1733\u1742\u1753\u1762")
        buf.write("\u176e\u1770\u1772\u1782\u17b5\u17d9\u17d9\u17de\u17de")
        buf.write("\u1822\u1879\u1882\u18aa\u1902\u191e\u1952\u196f\u1972")
        buf.write("\u1976\u1982\u19ab\u19c3\u19c9\u1a02\u1a18\u1d02\u1dc1")
        buf.write("\u1e02\u1e9d\u1ea2\u1efb\u1f02\u1f17\u1f1a\u1f1f\u1f22")
        buf.write("\u1f47\u1f4a\u1f4f\u1f52\u1f59\u1f5b\u1f5b\u1f5d\u1f5d")
        buf.write("\u1f5f\u1f5f\u1f61\u1f7f\u1f82\u1fb6\u1fb8\u1fbe\u1fc0")
        buf.write("\u1fc0\u1fc4\u1fc6\u1fc8\u1fce\u1fd2\u1fd5\u1fd8\u1fdd")
        buf.write("\u1fe2\u1fee\u1ff4\u1ff6\u1ff8\u1ffe\u2073\u2073\u2081")
        buf.write("\u2081\u2092\u2096\u2104\u2104\u2109\u2109\u210c\u2115")
        buf.write("\u2117\u2117\u211a\u211f\u2126\u2126\u2128\u2128\u212a")
        buf.write("\u212a\u212c\u2133\u2135\u213b\u213e\u2141\u2147\u214b")
        buf.write("\u2162\u2185\u2c02\u2c30\u2c32\u2c60\u2c82\u2ce6\u2d02")
        buf.write("\u2d27\u2d32\u2d67\u2d71\u2d71\u2d82\u2d98\u2da2\u2da8")
        buf.write("\u2daa\u2db0\u2db2\u2db8\u2dba\u2dc0\u2dc2\u2dc8\u2dca")
        buf.write("\u2dd0\u2dd2\u2dd8\u2dda\u2de0\u3007\u3009\u3023\u302b")
        buf.write("\u3033\u3037\u303a\u303e\u3043\u3098\u309d\u30a1\u30a3")
        buf.write("\u30fc\u30fe\u3101\u3107\u312e\u3133\u3190\u31a2\u31b9")
        buf.write("\u31f2\u3201\u3402\u4db7\u4e02\u9fbd\ua002\ua48e\ua802")
        buf.write("\ua803\ua805\ua807\ua809\ua80c\ua80e\ua824\uac02\ud7a5")
        buf.write("\uf902\ufa2f\ufa32\ufa6c\ufa72\ufadb\ufb02\ufb08\ufb15")
        buf.write("\ufb19\ufb1f\ufb1f\ufb21\ufb2a\ufb2c\ufb38\ufb3a\ufb3e")
        buf.write("\ufb40\ufb40\ufb42\ufb43\ufb45\ufb46\ufb48\ufbb3\ufbd5")
        buf.write("\ufd3f\ufd52\ufd91\ufd94\ufdc9\ufdf2\ufdfd\ufe72\ufe76")
        buf.write("\ufe78\ufefe\uff23\uff3c\uff43\uff5c\uff68\uffc0\uffc4")
        buf.write("\uffc9\uffcc\uffd1\uffd4\uffd9\uffdc\uffde\u0096\2\62")
        buf.write(";\u0302\u0371\u0485\u0488\u0593\u05bb\u05bd\u05bf\u05c1")
        buf.write("\u05c1\u05c3\u05c4\u05c6\u05c7\u05c9\u05c9\u0612\u0617")
        buf.write("\u064d\u0660\u0662\u066b\u0672\u0672\u06d8\u06de\u06e1")
        buf.write("\u06e6\u06e9\u06ea\u06ec\u06ef\u06f2\u06fb\u0713\u0713")
        buf.write("\u0732\u074c\u07a8\u07b2\u0903\u0905\u093e\u093e\u0940")
        buf.write("\u094f\u0953\u0956\u0964\u0965\u0968\u0971\u0983\u0985")
        buf.write("\u09be\u09be\u09c0\u09c6\u09c9\u09ca\u09cd\u09cf\u09d9")
        buf.write("\u09d9\u09e4\u09e5\u09e8\u09f1\u0a03\u0a05\u0a3e\u0a3e")
        buf.write("\u0a40\u0a44\u0a49\u0a4a\u0a4d\u0a4f\u0a68\u0a73\u0a83")
        buf.write("\u0a85\u0abe\u0abe\u0ac0\u0ac7\u0ac9\u0acb\u0acd\u0acf")
        buf.write("\u0ae4\u0ae5\u0ae8\u0af1\u0b03\u0b05\u0b3e\u0b3e\u0b40")
        buf.write("\u0b45\u0b49\u0b4a\u0b4d\u0b4f\u0b58\u0b59\u0b68\u0b71")
        buf.write("\u0b84\u0b84\u0bc0\u0bc4\u0bc8\u0bca\u0bcc\u0bcf\u0bd9")
        buf.write("\u0bd9\u0be8\u0bf1\u0c03\u0c05\u0c40\u0c46\u0c48\u0c4a")
        buf.write("\u0c4c\u0c4f\u0c57\u0c58\u0c68\u0c71\u0c84\u0c85\u0cbe")
        buf.write("\u0cbe\u0cc0\u0cc6\u0cc8\u0cca\u0ccc\u0ccf\u0cd7\u0cd8")
        buf.write("\u0ce8\u0cf1\u0d04\u0d05\u0d40\u0d45\u0d48\u0d4a\u0d4c")
        buf.write("\u0d4f\u0d59\u0d59\u0d68\u0d71\u0d84\u0d85\u0dcc\u0dcc")
        buf.write("\u0dd1\u0dd6\u0dd8\u0dd8\u0dda\u0de1\u0df4\u0df5\u0e33")
        buf.write("\u0e33\u0e36\u0e3c\u0e49\u0e50\u0e52\u0e5b\u0eb3\u0eb3")
        buf.write("\u0eb6\u0ebb\u0ebd\u0ebe\u0eca\u0ecf\u0ed2\u0edb\u0f1a")
        buf.write("\u0f1b\u0f22\u0f2b\u0f37\u0f37\u0f39\u0f39\u0f3b\u0f3b")
        buf.write("\u0f40\u0f41\u0f73\u0f86\u0f88\u0f89\u0f92\u0f99\u0f9b")
        buf.write("\u0fbe\u0fc8\u0fc8\u102e\u1034\u1038\u103b\u1042\u104b")
        buf.write("\u1058\u105b\u1361\u1361\u136b\u1373\u1714\u1716\u1734")
        buf.write("\u1736\u1754\u1755\u1774\u1775\u17b8\u17d5\u17df\u17df")
        buf.write("\u17e2\u17eb\u180d\u180f\u1812\u181b\u18ab\u18ab\u1922")
        buf.write("\u192d\u1932\u193d\u1948\u1951\u19b2\u19c2\u19ca\u19cb")
        buf.write("\u19d2\u19db\u1a19\u1a1d\u1dc2\u1dc5\u2041\u2042\u2056")
        buf.write("\u2056\u20d2\u20de\u20e3\u20e3\u20e7\u20ed\u302c\u3031")
        buf.write("\u309b\u309c\ua804\ua804\ua808\ua808\ua80d\ua80d\ua825")
        buf.write("\ua829\ufb20\ufb20\ufe02\ufe11\ufe22\ufe25\ufe35\ufe36")
        buf.write("\ufe4f\ufe51\uff12\uff1b\uff41\uff41\2\u039c\2\3\3\2\2")
        buf.write("\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2")
        buf.write("\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25")
        buf.write("\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3")
        buf.write("\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2")
        buf.write("\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2")
        buf.write("\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\2")
        buf.write("9\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2")
        buf.write("\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2")
        buf.write("\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2")
        buf.write("\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3")
        buf.write("\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2\2g\3\2\2\2\2i")
        buf.write("\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2q\3\2\2\2\2")
        buf.write("s\3\2\2\2\2u\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2")
        buf.write("\2}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2")
        buf.write("\2\2\2\u0085\3\2\2\2\2\u0087\3\2\2\2\2\u0089\3\2\2\2\2")
        buf.write("\u008b\3\2\2\2\2\u008d\3\2\2\2\2\u008f\3\2\2\2\2\u0091")
        buf.write("\3\2\2\2\2\u0093\3\2\2\2\2\u0095\3\2\2\2\2\u0097\3\2\2")
        buf.write("\2\2\u0099\3\2\2\2\2\u009b\3\2\2\2\2\u009d\3\2\2\2\2\u009f")
        buf.write("\3\2\2\2\2\u00a1\3\2\2\2\2\u00a3\3\2\2\2\2\u00a5\3\2\2")
        buf.write("\2\2\u00a7\3\2\2\2\2\u00a9\3\2\2\2\2\u00ab\3\2\2\2\2\u00ad")
        buf.write("\3\2\2\2\2\u00af\3\2\2\2\2\u00b1\3\2\2\2\2\u00b3\3\2\2")
        buf.write("\2\2\u00b5\3\2\2\2\2\u00b7\3\2\2\2\2\u00b9\3\2\2\2\2\u00bb")
        buf.write("\3\2\2\2\2\u00bd\3\2\2\2\2\u00bf\3\2\2\2\2\u00c1\3\2\2")
        buf.write("\2\2\u00c3\3\2\2\2\2\u00c5\3\2\2\2\2\u00c7\3\2\2\2\3\u00ff")
        buf.write("\3\2\2\2\5\u0105\3\2\2\2\7\u010b\3\2\2\2\t\u010d\3\2\2")
        buf.write("\2\13\u0110\3\2\2\2\r\u0117\3\2\2\2\17\u011d\3\2\2\2\21")
        buf.write("\u0122\3\2\2\2\23\u0129\3\2\2\2\25\u012c\3\2\2\2\27\u0133")
        buf.write("\3\2\2\2\31\u013c\3\2\2\2\33\u0143\3\2\2\2\35\u0146\3")
        buf.write("\2\2\2\37\u014b\3\2\2\2!\u0150\3\2\2\2#\u0156\3\2\2\2")
        buf.write("%\u0159\3\2\2\2\'\u015d\3\2\2\2)\u0160\3\2\2\2+\u0166")
        buf.write("\3\2\2\2-\u016a\3\2\2\2/\u0172\3\2\2\2\61\u0177\3\2\2")
        buf.write("\2\63\u017e\3\2\2\2\65\u0185\3\2\2\2\67\u0188\3\2\2\2")
        buf.write("9\u018c\3\2\2\2;\u0190\3\2\2\2=\u0193\3\2\2\2?\u0198\3")
        buf.write("\2\2\2A\u019d\3\2\2\2C\u01a3\3\2\2\2E\u01a9\3\2\2\2G\u01af")
        buf.write("\3\2\2\2I\u01b3\3\2\2\2K\u01b8\3\2\2\2M\u01c1\3\2\2\2")
        buf.write("O\u01c7\3\2\2\2Q\u01cd\3\2\2\2S\u01df\3\2\2\2U\u01e3\3")
        buf.write("\2\2\2W\u01ef\3\2\2\2Y\u01fa\3\2\2\2[\u020c\3\2\2\2]\u020e")
        buf.write("\3\2\2\2_\u0215\3\2\2\2a\u021c\3\2\2\2c\u0225\3\2\2\2")
        buf.write("e\u0229\3\2\2\2g\u022d\3\2\2\2i\u022f\3\2\2\2k\u0233\3")
        buf.write("\2\2\2m\u0235\3\2\2\2o\u0238\3\2\2\2q\u023b\3\2\2\2s\u023d")
        buf.write("\3\2\2\2u\u023f\3\2\2\2w\u0241\3\2\2\2y\u0244\3\2\2\2")
        buf.write("{\u0246\3\2\2\2}\u0249\3\2\2\2\177\u024c\3\2\2\2\u0081")
        buf.write("\u024e\3\2\2\2\u0083\u0250\3\2\2\2\u0085\u0252\3\2\2\2")
        buf.write("\u0087\u0255\3\2\2\2\u0089\u0258\3\2\2\2\u008b\u025a\3")
        buf.write("\2\2\2\u008d\u025c\3\2\2\2\u008f\u025e\3\2\2\2\u0091\u0260")
        buf.write("\3\2\2\2\u0093\u0263\3\2\2\2\u0095\u0265\3\2\2\2\u0097")
        buf.write("\u0268\3\2\2\2\u0099\u026b\3\2\2\2\u009b\u026d\3\2\2\2")
        buf.write("\u009d\u026f\3\2\2\2\u009f\u0272\3\2\2\2\u00a1\u0275\3")
        buf.write("\2\2\2\u00a3\u0278\3\2\2\2\u00a5\u027b\3\2\2\2\u00a7\u027e")
        buf.write("\3\2\2\2\u00a9\u0280\3\2\2\2\u00ab\u0283\3\2\2\2\u00ad")
        buf.write("\u0286\3\2\2\2\u00af\u0289\3\2\2\2\u00b1\u028c\3\2\2\2")
        buf.write("\u00b3\u028f\3\2\2\2\u00b5\u0292\3\2\2\2\u00b7\u0295\3")
        buf.write("\2\2\2\u00b9\u0298\3\2\2\2\u00bb\u029b\3\2\2\2\u00bd\u029e")
        buf.write("\3\2\2\2\u00bf\u02a2\3\2\2\2\u00c1\u02a6\3\2\2\2\u00c3")
        buf.write("\u02aa\3\2\2\2\u00c5\u02b1\3\2\2\2\u00c7\u02b5\3\2\2\2")
        buf.write("\u00c9\u02c9\3\2\2\2\u00cb\u02e5\3\2\2\2\u00cd\u02e9\3")
        buf.write("\2\2\2\u00cf\u02eb\3\2\2\2\u00d1\u02f1\3\2\2\2\u00d3\u02f3")
        buf.write("\3\2\2\2\u00d5\u02f5\3\2\2\2\u00d7\u02f7\3\2\2\2\u00d9")
        buf.write("\u02f9\3\2\2\2\u00db\u02fb\3\2\2\2\u00dd\u0304\3\2\2\2")
        buf.write("\u00df\u0308\3\2\2\2\u00e1\u030d\3\2\2\2\u00e3\u0311\3")
        buf.write("\2\2\2\u00e5\u0317\3\2\2\2\u00e7\u0332\3\2\2\2\u00e9\u034e")
        buf.write("\3\2\2\2\u00eb\u0352\3\2\2\2\u00ed\u0355\3\2\2\2\u00ef")
        buf.write("\u0358\3\2\2\2\u00f1\u035b\3\2\2\2\u00f3\u035d\3\2\2\2")
        buf.write("\u00f5\u0361\3\2\2\2\u00f7\u0365\3\2\2\2\u00f9\u036c\3")
        buf.write("\2\2\2\u00fb\u0378\3\2\2\2\u00fd\u037c\3\2\2\2\u00ff\u0100")
        buf.write("\7k\2\2\u0100\u0101\7u\2\2\u0101\u0102\7c\2\2\u0102\4")
        buf.write("\3\2\2\2\u0103\u0106\5W,\2\u0104\u0106\5Y-\2\u0105\u0103")
        buf.write("\3\2\2\2\u0105\u0104\3\2\2\2\u0106\6\3\2\2\2\u0107\u010c")
        buf.write("\5[.\2\u0108\u010c\5]/\2\u0109\u010c\5_\60\2\u010a\u010c")
        buf.write("\5a\61\2\u010b\u0107\3\2\2\2\u010b\u0108\3\2\2\2\u010b")
        buf.write("\u0109\3\2\2\2\u010b\u010a\3\2\2\2\u010c\b\3\2\2\2\u010d")
        buf.write("\u010e\7h\2\2\u010e\u010f\7p\2\2\u010f\n\3\2\2\2\u0110")
        buf.write("\u0111\7t\2\2\u0111\u0112\7g\2\2\u0112\u0113\7v\2\2\u0113")
        buf.write("\u0114\7w\2\2\u0114\u0115\7t\2\2\u0115\u0116\7p\2\2\u0116")
        buf.write("\f\3\2\2\2\u0117\u0118\7t\2\2\u0118\u0119\7c\2\2\u0119")
        buf.write("\u011a\7k\2\2\u011a\u011b\7u\2\2\u011b\u011c\7g\2\2\u011c")
        buf.write("\16\3\2\2\2\u011d\u011e\7h\2\2\u011e\u011f\7t\2\2\u011f")
        buf.write("\u0120\7q\2\2\u0120\u0121\7o\2\2\u0121\20\3\2\2\2\u0122")
        buf.write("\u0123\7k\2\2\u0123\u0124\7o\2\2\u0124\u0125\7r\2\2\u0125")
        buf.write("\u0126\7q\2\2\u0126\u0127\7t\2\2\u0127\u0128\7v\2\2\u0128")
        buf.write("\22\3\2\2\2\u0129\u012a\7c\2\2\u012a\u012b\7u\2\2\u012b")
        buf.write("\24\3\2\2\2\u012c\u012d\7i\2\2\u012d\u012e\7n\2\2\u012e")
        buf.write("\u012f\7q\2\2\u012f\u0130\7d\2\2\u0130\u0131\7c\2\2\u0131")
        buf.write("\u0132\7n\2\2\u0132\26\3\2\2\2\u0133\u0134\7p\2\2\u0134")
        buf.write("\u0135\7q\2\2\u0135\u0136\7p\2\2\u0136\u0137\7n\2\2\u0137")
        buf.write("\u0138\7q\2\2\u0138\u0139\7e\2\2\u0139\u013a\7c\2\2\u013a")
        buf.write("\u013b\7n\2\2\u013b\30\3\2\2\2\u013c\u013d\7c\2\2\u013d")
        buf.write("\u013e\7u\2\2\u013e\u013f\7u\2\2\u013f\u0140\7g\2\2\u0140")
        buf.write("\u0141\7t\2\2\u0141\u0142\7v\2\2\u0142\32\3\2\2\2\u0143")
        buf.write("\u0144\7k\2\2\u0144\u0145\7h\2\2\u0145\34\3\2\2\2\u0146")
        buf.write("\u0147\7g\2\2\u0147\u0148\7n\2\2\u0148\u0149\7k\2\2\u0149")
        buf.write("\u014a\7h\2\2\u014a\36\3\2\2\2\u014b\u014c\7g\2\2\u014c")
        buf.write("\u014d\7n\2\2\u014d\u014e\7u\2\2\u014e\u014f\7g\2\2\u014f")
        buf.write(" \3\2\2\2\u0150\u0151\7y\2\2\u0151\u0152\7j\2\2\u0152")
        buf.write("\u0153\7k\2\2\u0153\u0154\7n\2\2\u0154\u0155\7g\2\2\u0155")
        buf.write("\"\3\2\2\2\u0156\u0157\7f\2\2\u0157\u0158\7q\2\2\u0158")
        buf.write("$\3\2\2\2\u0159\u015a\7h\2\2\u015a\u015b\7q\2\2\u015b")
        buf.write("\u015c\7t\2\2\u015c&\3\2\2\2\u015d\u015e\7k\2\2\u015e")
        buf.write("\u015f\7p\2\2\u015f(\3\2\2\2\u0160\u0161\7e\2\2\u0161")
        buf.write("\u0162\7q\2\2\u0162\u0163\7p\2\2\u0163\u0164\7u\2\2\u0164")
        buf.write("\u0165\7v\2\2\u0165*\3\2\2\2\u0166\u0167\7v\2\2\u0167")
        buf.write("\u0168\7t\2\2\u0168\u0169\7{\2\2\u0169,\3\2\2\2\u016a")
        buf.write("\u016b\7h\2\2\u016b\u016c\7k\2\2\u016c\u016d\7p\2\2\u016d")
        buf.write("\u016e\7c\2\2\u016e\u016f\7n\2\2\u016f\u0170\7n\2\2\u0170")
        buf.write("\u0171\7{\2\2\u0171.\3\2\2\2\u0172\u0173\7y\2\2\u0173")
        buf.write("\u0174\7k\2\2\u0174\u0175\7v\2\2\u0175\u0176\7j\2\2\u0176")
        buf.write("\60\3\2\2\2\u0177\u0178\7g\2\2\u0178\u0179\7z\2\2\u0179")
        buf.write("\u017a\7e\2\2\u017a\u017b\7g\2\2\u017b\u017c\7r\2\2\u017c")
        buf.write("\u017d\7v\2\2\u017d\62\3\2\2\2\u017e\u017f\7n\2\2\u017f")
        buf.write("\u0180\7c\2\2\u0180\u0181\7o\2\2\u0181\u0182\7d\2\2\u0182")
        buf.write("\u0183\7f\2\2\u0183\u0184\7c\2\2\u0184\64\3\2\2\2\u0185")
        buf.write("\u0186\7q\2\2\u0186\u0187\7t\2\2\u0187\66\3\2\2\2\u0188")
        buf.write("\u0189\7c\2\2\u0189\u018a\7p\2\2\u018a\u018b\7f\2\2\u018b")
        buf.write("8\3\2\2\2\u018c\u018d\7p\2\2\u018d\u018e\7q\2\2\u018e")
        buf.write("\u018f\7v\2\2\u018f:\3\2\2\2\u0190\u0191\7k\2\2\u0191")
        buf.write("\u0192\7u\2\2\u0192<\3\2\2\2\u0193\u0194\7p\2\2\u0194")
        buf.write("\u0195\7q\2\2\u0195\u0196\7p\2\2\u0196\u0197\7g\2\2\u0197")
        buf.write(">\3\2\2\2\u0198\u0199\7v\2\2\u0199\u019a\7t\2\2\u019a")
        buf.write("\u019b\7w\2\2\u019b\u019c\7g\2\2\u019c@\3\2\2\2\u019d")
        buf.write("\u019e\7h\2\2\u019e\u019f\7c\2\2\u019f\u01a0\7n\2\2\u01a0")
        buf.write("\u01a1\7u\2\2\u01a1\u01a2\7g\2\2\u01a2B\3\2\2\2\u01a3")
        buf.write("\u01a4\7e\2\2\u01a4\u01a5\7n\2\2\u01a5\u01a6\7c\2\2\u01a6")
        buf.write("\u01a7\7u\2\2\u01a7\u01a8\7u\2\2\u01a8D\3\2\2\2\u01a9")
        buf.write("\u01aa\7{\2\2\u01aa\u01ab\7k\2\2\u01ab\u01ac\7g\2\2\u01ac")
        buf.write("\u01ad\7n\2\2\u01ad\u01ae\7f\2\2\u01aeF\3\2\2\2\u01af")
        buf.write("\u01b0\7f\2\2\u01b0\u01b1\7g\2\2\u01b1\u01b2\7n\2\2\u01b2")
        buf.write("H\3\2\2\2\u01b3\u01b4\7r\2\2\u01b4\u01b5\7c\2\2\u01b5")
        buf.write("\u01b6\7u\2\2\u01b6\u01b7\7u\2\2\u01b7J\3\2\2\2\u01b8")
        buf.write("\u01b9\7e\2\2\u01b9\u01ba\7q\2\2\u01ba\u01bb\7p\2\2\u01bb")
        buf.write("\u01bc\7v\2\2\u01bc\u01bd\7k\2\2\u01bd\u01be\7p\2\2\u01be")
        buf.write("\u01bf\7w\2\2\u01bf\u01c0\7g\2\2\u01c0L\3\2\2\2\u01c1")
        buf.write("\u01c2\7d\2\2\u01c2\u01c3\7t\2\2\u01c3\u01c4\7g\2\2\u01c4")
        buf.write("\u01c5\7c\2\2\u01c5\u01c6\7m\2\2\u01c6N\3\2\2\2\u01c7")
        buf.write("\u01c8\7c\2\2\u01c8\u01c9\7u\2\2\u01c9\u01ca\7{\2\2\u01ca")
        buf.write("\u01cb\7p\2\2\u01cb\u01cc\7e\2\2\u01ccP\3\2\2\2\u01cd")
        buf.write("\u01ce\7c\2\2\u01ce\u01cf\7y\2\2\u01cf\u01d0\7c\2\2\u01d0")
        buf.write("\u01d1\7k\2\2\u01d1\u01d2\7v\2\2\u01d2R\3\2\2\2\u01d3")
        buf.write("\u01d4\6*\2\2\u01d4\u01e0\5\u00f5{\2\u01d5\u01d7\7\17")
        buf.write("\2\2\u01d6\u01d5\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d7\u01d8")
        buf.write("\3\2\2\2\u01d8\u01db\7\f\2\2\u01d9\u01db\4\16\17\2\u01da")
        buf.write("\u01d6\3\2\2\2\u01da\u01d9\3\2\2\2\u01db\u01dd\3\2\2\2")
        buf.write("\u01dc\u01de\5\u00f5{\2\u01dd\u01dc\3\2\2\2\u01dd\u01de")
        buf.write("\3\2\2\2\u01de\u01e0\3\2\2\2\u01df\u01d3\3\2\2\2\u01df")
        buf.write("\u01da\3\2\2\2\u01e0\u01e1\3\2\2\2\u01e1\u01e2\b*\2\2")
        buf.write("\u01e2T\3\2\2\2\u01e3\u01e7\5\u00fb~\2\u01e4\u01e6\5\u00fd")
        buf.write("\177\2\u01e5\u01e4\3\2\2\2\u01e6\u01e9\3\2\2\2\u01e7\u01e5")
        buf.write("\3\2\2\2\u01e7\u01e8\3\2\2\2\u01e8V\3\2\2\2\u01e9\u01e7")
        buf.write("\3\2\2\2\u01ea\u01f0\t\2\2\2\u01eb\u01ec\t\3\2\2\u01ec")
        buf.write("\u01f0\t\4\2\2\u01ed\u01ee\t\4\2\2\u01ee\u01f0\t\3\2\2")
        buf.write("\u01ef\u01ea\3\2\2\2\u01ef\u01eb\3\2\2\2\u01ef\u01ed\3")
        buf.write("\2\2\2\u01ef\u01f0\3\2\2\2\u01f0\u01f3\3\2\2\2\u01f1\u01f4")
        buf.write("\5\u00c9e\2\u01f2\u01f4\5\u00cbf\2\u01f3\u01f1\3\2\2\2")
        buf.write("\u01f3\u01f2\3\2\2\2\u01f4X\3\2\2\2\u01f5\u01fb\t\5\2")
        buf.write("\2\u01f6\u01f7\t\5\2\2\u01f7\u01fb\t\4\2\2\u01f8\u01f9")
        buf.write("\t\4\2\2\u01f9\u01fb\t\5\2\2\u01fa\u01f5\3\2\2\2\u01fa")
        buf.write("\u01f6\3\2\2\2\u01fa\u01f8\3\2\2\2\u01fb\u01fe\3\2\2\2")
        buf.write("\u01fc\u01ff\5\u00e7t\2\u01fd\u01ff\5\u00e9u\2\u01fe\u01fc")
        buf.write("\3\2\2\2\u01fe\u01fd\3\2\2\2\u01ffZ\3\2\2\2\u0200\u0204")
        buf.write("\5\u00d3j\2\u0201\u0203\5\u00d5k\2\u0202\u0201\3\2\2\2")
        buf.write("\u0203\u0206\3\2\2\2\u0204\u0202\3\2\2\2\u0204\u0205\3")
        buf.write("\2\2\2\u0205\u020d\3\2\2\2\u0206\u0204\3\2\2\2\u0207\u0209")
        buf.write("\7\62\2\2\u0208\u0207\3\2\2\2\u0209\u020a\3\2\2\2\u020a")
        buf.write("\u0208\3\2\2\2\u020a\u020b\3\2\2\2\u020b\u020d\3\2\2\2")
        buf.write("\u020c\u0200\3\2\2\2\u020c\u0208\3\2\2\2\u020d\\\3\2\2")
        buf.write("\2\u020e\u020f\7\62\2\2\u020f\u0211\t\6\2\2\u0210\u0212")
        buf.write("\5\u00d7l\2\u0211\u0210\3\2\2\2\u0212\u0213\3\2\2\2\u0213")
        buf.write("\u0211\3\2\2\2\u0213\u0214\3\2\2\2\u0214^\3\2\2\2\u0215")
        buf.write("\u0216\7\62\2\2\u0216\u0218\t\7\2\2\u0217\u0219\5\u00d9")
        buf.write("m\2\u0218\u0217\3\2\2\2\u0219\u021a\3\2\2\2\u021a\u0218")
        buf.write("\3\2\2\2\u021a\u021b\3\2\2\2\u021b`\3\2\2\2\u021c\u021d")
        buf.write("\7\62\2\2\u021d\u021f\t\5\2\2\u021e\u0220\5\u00dbn\2\u021f")
        buf.write("\u021e\3\2\2\2\u0220\u0221\3\2\2\2\u0221\u021f\3\2\2\2")
        buf.write("\u0221\u0222\3\2\2\2\u0222b\3\2\2\2\u0223\u0226\5\u00dd")
        buf.write("o\2\u0224\u0226\5\u00dfp\2\u0225\u0223\3\2\2\2\u0225\u0224")
        buf.write("\3\2\2\2\u0226d\3\2\2\2\u0227\u022a\5c\62\2\u0228\u022a")
        buf.write("\5\u00e1q\2\u0229\u0227\3\2\2\2\u0229\u0228\3\2\2\2\u022a")
        buf.write("\u022b\3\2\2\2\u022b\u022c\t\b\2\2\u022cf\3\2\2\2\u022d")
        buf.write("\u022e\7\60\2\2\u022eh\3\2\2\2\u022f\u0230\7\60\2\2\u0230")
        buf.write("\u0231\7\60\2\2\u0231\u0232\7\60\2\2\u0232j\3\2\2\2\u0233")
        buf.write("\u0234\7,\2\2\u0234l\3\2\2\2\u0235\u0236\7*\2\2\u0236")
        buf.write("\u0237\b\67\3\2\u0237n\3\2\2\2\u0238\u0239\7+\2\2\u0239")
        buf.write("\u023a\b8\4\2\u023ap\3\2\2\2\u023b\u023c\7.\2\2\u023c")
        buf.write("r\3\2\2\2\u023d\u023e\7<\2\2\u023et\3\2\2\2\u023f\u0240")
        buf.write("\7=\2\2\u0240v\3\2\2\2\u0241\u0242\7,\2\2\u0242\u0243")
        buf.write("\7,\2\2\u0243x\3\2\2\2\u0244\u0245\7?\2\2\u0245z\3\2\2")
        buf.write("\2\u0246\u0247\7]\2\2\u0247\u0248\b>\5\2\u0248|\3\2\2")
        buf.write("\2\u0249\u024a\7_\2\2\u024a\u024b\b?\6\2\u024b~\3\2\2")
        buf.write("\2\u024c\u024d\7~\2\2\u024d\u0080\3\2\2\2\u024e\u024f")
        buf.write("\7`\2\2\u024f\u0082\3\2\2\2\u0250\u0251\7(\2\2\u0251\u0084")
        buf.write("\3\2\2\2\u0252\u0253\7>\2\2\u0253\u0254\7>\2\2\u0254\u0086")
        buf.write("\3\2\2\2\u0255\u0256\7@\2\2\u0256\u0257\7@\2\2\u0257\u0088")
        buf.write("\3\2\2\2\u0258\u0259\7-\2\2\u0259\u008a\3\2\2\2\u025a")
        buf.write("\u025b\7/\2\2\u025b\u008c\3\2\2\2\u025c\u025d\7\61\2\2")
        buf.write("\u025d\u008e\3\2\2\2\u025e\u025f\7\'\2\2\u025f\u0090\3")
        buf.write("\2\2\2\u0260\u0261\7\61\2\2\u0261\u0262\7\61\2\2\u0262")
        buf.write("\u0092\3\2\2\2\u0263\u0264\7\u0080\2\2\u0264\u0094\3\2")
        buf.write("\2\2\u0265\u0266\7}\2\2\u0266\u0267\bK\7\2\u0267\u0096")
        buf.write("\3\2\2\2\u0268\u0269\7\177\2\2\u0269\u026a\bL\b\2\u026a")
        buf.write("\u0098\3\2\2\2\u026b\u026c\7>\2\2\u026c\u009a\3\2\2\2")
        buf.write("\u026d\u026e\7@\2\2\u026e\u009c\3\2\2\2\u026f\u0270\7")
        buf.write("?\2\2\u0270\u0271\7?\2\2\u0271\u009e\3\2\2\2\u0272\u0273")
        buf.write("\7@\2\2\u0273\u0274\7?\2\2\u0274\u00a0\3\2\2\2\u0275\u0276")
        buf.write("\7>\2\2\u0276\u0277\7?\2\2\u0277\u00a2\3\2\2\2\u0278\u0279")
        buf.write("\7>\2\2\u0279\u027a\7@\2\2\u027a\u00a4\3\2\2\2\u027b\u027c")
        buf.write("\7#\2\2\u027c\u027d\7?\2\2\u027d\u00a6\3\2\2\2\u027e\u027f")
        buf.write("\7B\2\2\u027f\u00a8\3\2\2\2\u0280\u0281\7/\2\2\u0281\u0282")
        buf.write("\7@\2\2\u0282\u00aa\3\2\2\2\u0283\u0284\7-\2\2\u0284\u0285")
        buf.write("\7?\2\2\u0285\u00ac\3\2\2\2\u0286\u0287\7/\2\2\u0287\u0288")
        buf.write("\7?\2\2\u0288\u00ae\3\2\2\2\u0289\u028a\7,\2\2\u028a\u028b")
        buf.write("\7?\2\2\u028b\u00b0\3\2\2\2\u028c\u028d\7B\2\2\u028d\u028e")
        buf.write("\7?\2\2\u028e\u00b2\3\2\2\2\u028f\u0290\7\61\2\2\u0290")
        buf.write("\u0291\7?\2\2\u0291\u00b4\3\2\2\2\u0292\u0293\7\'\2\2")
        buf.write("\u0293\u0294\7?\2\2\u0294\u00b6\3\2\2\2\u0295\u0296\7")
        buf.write("(\2\2\u0296\u0297\7?\2\2\u0297\u00b8\3\2\2\2\u0298\u0299")
        buf.write("\7~\2\2\u0299\u029a\7?\2\2\u029a\u00ba\3\2\2\2\u029b\u029c")
        buf.write("\7`\2\2\u029c\u029d\7?\2\2\u029d\u00bc\3\2\2\2\u029e\u029f")
        buf.write("\7>\2\2\u029f\u02a0\7>\2\2\u02a0\u02a1\7?\2\2\u02a1\u00be")
        buf.write("\3\2\2\2\u02a2\u02a3\7@\2\2\u02a3\u02a4\7@\2\2\u02a4\u02a5")
        buf.write("\7?\2\2\u02a5\u00c0\3\2\2\2\u02a6\u02a7\7,\2\2\u02a7\u02a8")
        buf.write("\7,\2\2\u02a8\u02a9\7?\2\2\u02a9\u00c2\3\2\2\2\u02aa\u02ab")
        buf.write("\7\61\2\2\u02ab\u02ac\7\61\2\2\u02ac\u02ad\7?\2\2\u02ad")
        buf.write("\u00c4\3\2\2\2\u02ae\u02b2\5\u00f5{\2\u02af\u02b2\5\u00f7")
        buf.write("|\2\u02b0\u02b2\5\u00f9}\2\u02b1\u02ae\3\2\2\2\u02b1\u02af")
        buf.write("\3\2\2\2\u02b1\u02b0\3\2\2\2\u02b2\u02b3\3\2\2\2\u02b3")
        buf.write("\u02b4\bc\t\2\u02b4\u00c6\3\2\2\2\u02b5\u02b6\13\2\2\2")
        buf.write("\u02b6\u00c8\3\2\2\2\u02b7\u02bc\7)\2\2\u02b8\u02bb\5")
        buf.write("\u00d1i\2\u02b9\u02bb\n\t\2\2\u02ba\u02b8\3\2\2\2\u02ba")
        buf.write("\u02b9\3\2\2\2\u02bb\u02be\3\2\2\2\u02bc\u02ba\3\2\2\2")
        buf.write("\u02bc\u02bd\3\2\2\2\u02bd\u02bf\3\2\2\2\u02be\u02bc\3")
        buf.write("\2\2\2\u02bf\u02ca\7)\2\2\u02c0\u02c5\7$\2\2\u02c1\u02c4")
        buf.write("\5\u00d1i\2\u02c2\u02c4\n\n\2\2\u02c3\u02c1\3\2\2\2\u02c3")
        buf.write("\u02c2\3\2\2\2\u02c4\u02c7\3\2\2\2\u02c5\u02c3\3\2\2\2")
        buf.write("\u02c5\u02c6\3\2\2\2\u02c6\u02c8\3\2\2\2\u02c7\u02c5\3")
        buf.write("\2\2\2\u02c8\u02ca\7$\2\2\u02c9\u02b7\3\2\2\2\u02c9\u02c0")
        buf.write("\3\2\2\2\u02ca\u00ca\3\2\2\2\u02cb\u02cc\7)\2\2\u02cc")
        buf.write("\u02cd\7)\2\2\u02cd\u02ce\7)\2\2\u02ce\u02d2\3\2\2\2\u02cf")
        buf.write("\u02d1\5\u00cdg\2\u02d0\u02cf\3\2\2\2\u02d1\u02d4\3\2")
        buf.write("\2\2\u02d2\u02d3\3\2\2\2\u02d2\u02d0\3\2\2\2\u02d3\u02d5")
        buf.write("\3\2\2\2\u02d4\u02d2\3\2\2\2\u02d5\u02d6\7)\2\2\u02d6")
        buf.write("\u02d7\7)\2\2\u02d7\u02e6\7)\2\2\u02d8\u02d9\7$\2\2\u02d9")
        buf.write("\u02da\7$\2\2\u02da\u02db\7$\2\2\u02db\u02df\3\2\2\2\u02dc")
        buf.write("\u02de\5\u00cdg\2\u02dd\u02dc\3\2\2\2\u02de\u02e1\3\2")
        buf.write("\2\2\u02df\u02e0\3\2\2\2\u02df\u02dd\3\2\2\2\u02e0\u02e2")
        buf.write("\3\2\2\2\u02e1\u02df\3\2\2\2\u02e2\u02e3\7$\2\2\u02e3")
        buf.write("\u02e4\7$\2\2\u02e4\u02e6\7$\2\2\u02e5\u02cb\3\2\2\2\u02e5")
        buf.write("\u02d8\3\2\2\2\u02e6\u00cc\3\2\2\2\u02e7\u02ea\5\u00cf")
        buf.write("h\2\u02e8\u02ea\5\u00d1i\2\u02e9\u02e7\3\2\2\2\u02e9\u02e8")
        buf.write("\3\2\2\2\u02ea\u00ce\3\2\2\2\u02eb\u02ec\n\13\2\2\u02ec")
        buf.write("\u00d0\3\2\2\2\u02ed\u02ee\7^\2\2\u02ee\u02f2\13\2\2\2")
        buf.write("\u02ef\u02f0\7^\2\2\u02f0\u02f2\5S*\2\u02f1\u02ed\3\2")
        buf.write("\2\2\u02f1\u02ef\3\2\2\2\u02f2\u00d2\3\2\2\2\u02f3\u02f4")
        buf.write("\t\f\2\2\u02f4\u00d4\3\2\2\2\u02f5\u02f6\t\r\2\2\u02f6")
        buf.write("\u00d6\3\2\2\2\u02f7\u02f8\t\16\2\2\u02f8\u00d8\3\2\2")
        buf.write("\2\u02f9\u02fa\t\17\2\2\u02fa\u00da\3\2\2\2\u02fb\u02fc")
        buf.write("\t\20\2\2\u02fc\u00dc\3\2\2\2\u02fd\u02ff\5\u00e1q\2\u02fe")
        buf.write("\u02fd\3\2\2\2\u02fe\u02ff\3\2\2\2\u02ff\u0300\3\2\2\2")
        buf.write("\u0300\u0305\5\u00e3r\2\u0301\u0302\5\u00e1q\2\u0302\u0303")
        buf.write("\7\60\2\2\u0303\u0305\3\2\2\2\u0304\u02fe\3\2\2\2\u0304")
        buf.write("\u0301\3\2\2\2\u0305\u00de\3\2\2\2\u0306\u0309\5\u00e1")
        buf.write("q\2\u0307\u0309\5\u00ddo\2\u0308\u0306\3\2\2\2\u0308\u0307")
        buf.write("\3\2\2\2\u0309\u030a\3\2\2\2\u030a\u030b\5\u00e5s\2\u030b")
        buf.write("\u00e0\3\2\2\2\u030c\u030e\5\u00d5k\2\u030d\u030c\3\2")
        buf.write("\2\2\u030e\u030f\3\2\2\2\u030f\u030d\3\2\2\2\u030f\u0310")
        buf.write("\3\2\2\2\u0310\u00e2\3\2\2\2\u0311\u0313\7\60\2\2\u0312")
        buf.write("\u0314\5\u00d5k\2\u0313\u0312\3\2\2\2\u0314\u0315\3\2")
        buf.write("\2\2\u0315\u0313\3\2\2\2\u0315\u0316\3\2\2\2\u0316\u00e4")
        buf.write("\3\2\2\2\u0317\u0319\t\21\2\2\u0318\u031a\t\22\2\2\u0319")
        buf.write("\u0318\3\2\2\2\u0319\u031a\3\2\2\2\u031a\u031c\3\2\2\2")
        buf.write("\u031b\u031d\5\u00d5k\2\u031c\u031b\3\2\2\2\u031d\u031e")
        buf.write("\3\2\2\2\u031e\u031c\3\2\2\2\u031e\u031f\3\2\2\2\u031f")
        buf.write("\u00e6\3\2\2\2\u0320\u0325\7)\2\2\u0321\u0324\5\u00ed")
        buf.write("w\2\u0322\u0324\5\u00f3z\2\u0323\u0321\3\2\2\2\u0323\u0322")
        buf.write("\3\2\2\2\u0324\u0327\3\2\2\2\u0325\u0323\3\2\2\2\u0325")
        buf.write("\u0326\3\2\2\2\u0326\u0328\3\2\2\2\u0327\u0325\3\2\2\2")
        buf.write("\u0328\u0333\7)\2\2\u0329\u032e\7$\2\2\u032a\u032d\5\u00ef")
        buf.write("x\2\u032b\u032d\5\u00f3z\2\u032c\u032a\3\2\2\2\u032c\u032b")
        buf.write("\3\2\2\2\u032d\u0330\3\2\2\2\u032e\u032c\3\2\2\2\u032e")
        buf.write("\u032f\3\2\2\2\u032f\u0331\3\2\2\2\u0330\u032e\3\2\2\2")
        buf.write("\u0331\u0333\7$\2\2\u0332\u0320\3\2\2\2\u0332\u0329\3")
        buf.write("\2\2\2\u0333\u00e8\3\2\2\2\u0334\u0335\7)\2\2\u0335\u0336")
        buf.write("\7)\2\2\u0336\u0337\7)\2\2\u0337\u033b\3\2\2\2\u0338\u033a")
        buf.write("\5\u00ebv\2\u0339\u0338\3\2\2\2\u033a\u033d\3\2\2\2\u033b")
        buf.write("\u033c\3\2\2\2\u033b\u0339\3\2\2\2\u033c\u033e\3\2\2\2")
        buf.write("\u033d\u033b\3\2\2\2\u033e\u033f\7)\2\2\u033f\u0340\7")
        buf.write(")\2\2\u0340\u034f\7)\2\2\u0341\u0342\7$\2\2\u0342\u0343")
        buf.write("\7$\2\2\u0343\u0344\7$\2\2\u0344\u0348\3\2\2\2\u0345\u0347")
        buf.write("\5\u00ebv\2\u0346\u0345\3\2\2\2\u0347\u034a\3\2\2\2\u0348")
        buf.write("\u0349\3\2\2\2\u0348\u0346\3\2\2\2\u0349\u034b\3\2\2\2")
        buf.write("\u034a\u0348\3\2\2\2\u034b\u034c\7$\2\2\u034c\u034d\7")
        buf.write("$\2\2\u034d\u034f\7$\2\2\u034e\u0334\3\2\2\2\u034e\u0341")
        buf.write("\3\2\2\2\u034f\u00ea\3\2\2\2\u0350\u0353\5\u00f1y\2\u0351")
        buf.write("\u0353\5\u00f3z\2\u0352\u0350\3\2\2\2\u0352\u0351\3\2")
        buf.write("\2\2\u0353\u00ec\3\2\2\2\u0354\u0356\t\23\2\2\u0355\u0354")
        buf.write("\3\2\2\2\u0356\u00ee\3\2\2\2\u0357\u0359\t\24\2\2\u0358")
        buf.write("\u0357\3\2\2\2\u0359\u00f0\3\2\2\2\u035a\u035c\t\25\2")
        buf.write("\2\u035b\u035a\3\2\2\2\u035c\u00f2\3\2\2\2\u035d\u035e")
        buf.write("\7^\2\2\u035e\u035f\t\26\2\2\u035f\u00f4\3\2\2\2\u0360")
        buf.write("\u0362\t\27\2\2\u0361\u0360\3\2\2\2\u0362\u0363\3\2\2")
        buf.write("\2\u0363\u0361\3\2\2\2\u0363\u0364\3\2\2\2\u0364\u00f6")
        buf.write("\3\2\2\2\u0365\u0369\7%\2\2\u0366\u0368\n\30\2\2\u0367")
        buf.write("\u0366\3\2\2\2\u0368\u036b\3\2\2\2\u0369\u0367\3\2\2\2")
        buf.write("\u0369\u036a\3\2\2\2\u036a\u00f8\3\2\2\2\u036b\u0369\3")
        buf.write("\2\2\2\u036c\u036e\7^\2\2\u036d\u036f\5\u00f5{\2\u036e")
        buf.write("\u036d\3\2\2\2\u036e\u036f\3\2\2\2\u036f\u0375\3\2\2\2")
        buf.write("\u0370\u0372\7\17\2\2\u0371\u0370\3\2\2\2\u0371\u0372")
        buf.write("\3\2\2\2\u0372\u0373\3\2\2\2\u0373\u0376\7\f\2\2\u0374")
        buf.write("\u0376\4\16\17\2\u0375\u0371\3\2\2\2\u0375\u0374\3\2\2")
        buf.write("\2\u0376\u00fa\3\2\2\2\u0377\u0379\t\31\2\2\u0378\u0377")
        buf.write("\3\2\2\2\u0379\u00fc\3\2\2\2\u037a\u037d\5\u00fb~\2\u037b")
        buf.write("\u037d\t\32\2\2\u037c\u037a\3\2\2\2\u037c\u037b\3\2\2")
        buf.write("\2\u037d\u00fe\3\2\2\2;\2\u0105\u010b\u01d6\u01da\u01dd")
        buf.write("\u01df\u01e7\u01ef\u01f3\u01fa\u01fe\u0204\u020a\u020c")
        buf.write("\u0213\u021a\u0221\u0225\u0229\u02b1\u02ba\u02bc\u02c3")
        buf.write("\u02c5\u02c9\u02d2\u02df\u02e5\u02e9\u02f1\u02fe\u0304")
        buf.write("\u0308\u030f\u0315\u0319\u031e\u0323\u0325\u032c\u032e")
        buf.write("\u0332\u033b\u0348\u034e\u0352\u0355\u0358\u035b\u0363")
        buf.write("\u0369\u036e\u0371\u0375\u0378\u037c\n\3*\2\3\67\3\38")
        buf.write("\4\3>\5\3?\6\3K\7\3L\b\b\2\2")
        return buf.getvalue()


class DrakeLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    STRING = 2
    INTEGER = 3
    FN = 4
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
    DO = 17
    FOR = 18
    IN = 19
    CONST = 20
    TRY = 21
    FINALLY = 22
    WITH = 23
    EXCEPT = 24
    LAMBDA = 25
    OR = 26
    AND = 27
    NOT = 28
    IS = 29
    NONE = 30
    TRUE = 31
    FALSE = 32
    CLASS = 33
    YIELD = 34
    DEL = 35
    PASS = 36
    CONTINUE = 37
    BREAK = 38
    ASYNC = 39
    AWAIT = 40
    NEWLINE = 41
    NAME = 42
    STRING_LITERAL = 43
    BYTES_LITERAL = 44
    DECIMAL_INTEGER = 45
    OCT_INTEGER = 46
    HEX_INTEGER = 47
    BIN_INTEGER = 48
    FLOAT_NUMBER = 49
    IMAG_NUMBER = 50
    DOT = 51
    ELLIPSIS = 52
    STAR = 53
    OPEN_PAREN = 54
    CLOSE_PAREN = 55
    COMMA = 56
    COLON = 57
    SEMI_COLON = 58
    POWER = 59
    ASSIGN = 60
    OPEN_BRACK = 61
    CLOSE_BRACK = 62
    OR_OP = 63
    XOR = 64
    AND_OP = 65
    LEFT_SHIFT = 66
    RIGHT_SHIFT = 67
    ADD = 68
    MINUS = 69
    DIV = 70
    MOD = 71
    IDIV = 72
    NOT_OP = 73
    OPEN_BRACE = 74
    CLOSE_BRACE = 75
    LESS_THAN = 76
    GREATER_THAN = 77
    EQUALS = 78
    GT_EQ = 79
    LT_EQ = 80
    NOT_EQ_1 = 81
    NOT_EQ_2 = 82
    AT = 83
    ARROW = 84
    ADD_ASSIGN = 85
    SUB_ASSIGN = 86
    MULT_ASSIGN = 87
    AT_ASSIGN = 88
    DIV_ASSIGN = 89
    MOD_ASSIGN = 90
    AND_ASSIGN = 91
    OR_ASSIGN = 92
    XOR_ASSIGN = 93
    LEFT_SHIFT_ASSIGN = 94
    RIGHT_SHIFT_ASSIGN = 95
    POWER_ASSIGN = 96
    IDIV_ASSIGN = 97
    SKIP_ = 98
    UNKNOWN_CHAR = 99

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'isa'", "'fn'", "'return'", "'raise'", "'from'", "'import'", 
            "'as'", "'global'", "'nonlocal'", "'assert'", "'if'", "'elif'", 
            "'else'", "'while'", "'do'", "'for'", "'in'", "'const'", "'try'", 
            "'finally'", "'with'", "'except'", "'lambda'", "'or'", "'and'", 
            "'not'", "'is'", "'none'", "'true'", "'false'", "'class'", "'yield'", 
            "'del'", "'pass'", "'continue'", "'break'", "'async'", "'await'", 
            "'.'", "'...'", "'*'", "'('", "')'", "','", "':'", "';'", "'**'", 
            "'='", "'['", "']'", "'|'", "'^'", "'&'", "'<<'", "'>>'", "'+'", 
            "'-'", "'/'", "'%'", "'//'", "'~'", "'{'", "'}'", "'<'", "'>'", 
            "'=='", "'>='", "'<='", "'<>'", "'!='", "'@'", "'->'", "'+='", 
            "'-='", "'*='", "'@='", "'/='", "'%='", "'&='", "'|='", "'^='", 
            "'<<='", "'>>='", "'**='", "'//='" ]

    symbolicNames = [ "<INVALID>",
            "STRING", "INTEGER", "FN", "RETURN", "RAISE", "FROM", "IMPORT", 
            "AS", "GLOBAL", "NONLOCAL", "ASSERT", "IF", "ELIF", "ELSE", 
            "WHILE", "DO", "FOR", "IN", "CONST", "TRY", "FINALLY", "WITH", 
            "EXCEPT", "LAMBDA", "OR", "AND", "NOT", "IS", "NONE", "TRUE", 
            "FALSE", "CLASS", "YIELD", "DEL", "PASS", "CONTINUE", "BREAK", 
            "ASYNC", "AWAIT", "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
            "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
            "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", "OPEN_PAREN", 
            "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", "POWER", "ASSIGN", 
            "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", "AND_OP", "LEFT_SHIFT", 
            "RIGHT_SHIFT", "ADD", "MINUS", "DIV", "MOD", "IDIV", "NOT_OP", 
            "OPEN_BRACE", "CLOSE_BRACE", "LESS_THAN", "GREATER_THAN", "EQUALS", 
            "GT_EQ", "LT_EQ", "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", 
            "SUB_ASSIGN", "MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", 
            "AND_ASSIGN", "OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", 
            "RIGHT_SHIFT_ASSIGN", "POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", 
            "UNKNOWN_CHAR" ]

    ruleNames = [ "T__0", "STRING", "INTEGER", "FN", "RETURN", "RAISE", 
                  "FROM", "IMPORT", "AS", "GLOBAL", "NONLOCAL", "ASSERT", 
                  "IF", "ELIF", "ELSE", "WHILE", "DO", "FOR", "IN", "CONST", 
                  "TRY", "FINALLY", "WITH", "EXCEPT", "LAMBDA", "OR", "AND", 
                  "NOT", "IS", "NONE", "TRUE", "FALSE", "CLASS", "YIELD", 
                  "DEL", "PASS", "CONTINUE", "BREAK", "ASYNC", "AWAIT", 
                  "NEWLINE", "NAME", "STRING_LITERAL", "BYTES_LITERAL", 
                  "DECIMAL_INTEGER", "OCT_INTEGER", "HEX_INTEGER", "BIN_INTEGER", 
                  "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", "STAR", 
                  "OPEN_PAREN", "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", 
                  "POWER", "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", 
                  "XOR", "AND_OP", "LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", 
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
            actions[40] = self.NEWLINE_action 
            actions[53] = self.OPEN_PAREN_action 
            actions[54] = self.CLOSE_PAREN_action 
            actions[60] = self.OPEN_BRACK_action 
            actions[61] = self.CLOSE_BRACK_action 
            actions[73] = self.OPEN_BRACE_action 
            actions[74] = self.CLOSE_BRACE_action 
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
                    # self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        # self.emitToken(self.createDedent())
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
            preds[40] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


