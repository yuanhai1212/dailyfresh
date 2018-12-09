# # class Solution(object):
# #     def isValid(self, s):
# #         """
# #         :type s: str
# #         :rtype: bool
# #         """
# #
# #         # The stack to keep track of opening brackets.
# #         stack = []
# #
# #         # Hash map for keeping track of mappings. This keeps the code very clean.
# #         # Also makes adding more types of parenthesis easier
# #         mapping = {")": "(", "}": "{", "]": "["}
# #
# #         for i in s:
# #             if i in mapping:
# #
# #                 top_num = stack.pop()if stack else "#"
# #
# #                 if mapping[i] !=top_num:
# #                     return False
# #             else:
# #                 stack.append(i)
# #         return not stack
# #
# # a = Solution()
# # print(a.isValid('[{()}]'))
# from urllib import request,parse
#
# url='https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
# headers =  {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }
# data = {
#     'first':'true',
#     'pn':1,
#     'kd':'python'
# }
# req = request.Request(url,headers=headers,data=parse.urlencode(data).encode('utf-8'),method='POST')
# resp= request.urlopen(req)
# print(resp.read())