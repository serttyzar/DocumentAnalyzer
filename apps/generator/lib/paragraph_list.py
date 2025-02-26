from docx.text.paragraph import Paragraph


class ParagraphExt(Paragraph):

    p = None

    def __init__(self, p: Paragraph):
        super().__init__(p._element, p._parent)
        self.p = p

    def restart_numbering(self):
        """
        Restarting the numbering of paragraph
        """
        # Getting the abstract number of paragraph
        abstract_num_id = self.p.part.document.part.numbering_part.element.num_having_numId(
            self.p.style.element.get_or_add_pPr().get_or_add_numPr().numId.val).abstractNumId.val

        # Add abstract number to numbering part and reset
        num = self.p.part.numbering_part.element.add_num(abstract_num_id)
        num.add_lvlOverride(ilvl=0).add_startOverride(1)

        # Get or add elements to paragraph
        p_pr = self.p._p.get_or_add_pPr()
        num_pr = p_pr.get_or_add_numPr()
        ilvl = num_pr.get_or_add_ilvl()
        ilvl.val = int("0")
        num_id = num_pr.get_or_add_numId()
        num_id.val = int(num.numId)